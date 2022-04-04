import asyncio
import requests
import random
import json
import time
import os
import re

import src.database as db


def get_office_id():
    return requests.get('http://web/statevector/office_id').text

def check_election_state_running() -> bool:
    r = requests.get('http://web/statevector/state_election').text

    return r == '1'


def check_terminals_regitration_running() -> bool:
    r = requests.get('http://web/statevector/state_register_terminals').text

    return r == '1'

async def get_terminals() -> list[dict[str, str]]:
    return await db.keys_collection.find().to_list(None)


async def insert_local_vt_if_env() -> None:
    try:
        if os.environ['TEST_INSERT_VT'] == 'True':
            await db.keys_collection.insert_one({
                '_id': 'TEST_VT_ID',
                'public_key': 'TEST_VT_PUBLIC_KEY',
                'ip': os.environ["TEST_INSERT_VT_IP"],
            })

    except KeyError:
        pass


async def get_unique_vt_id(office_id):
    vt_id = f'{office_id}:{random.randint(0, 1000000):06d}'
    while await db.keys_collection.count_documents({'_id': vt_id}):
        print('VT id already exists', vt_id)
        time.sleep(0.1)

        vt_id = f'{office_id}:{random.randint(0, 1000000):06d}'

    return vt_id


def get_public_key():
    key = requests.get('http://web/temporary_key_location/public_key.txt').text

    return key


def get_config():
    polling_place_id = int(get_office_id())

    response = requests.get("http://web/statevector/config/config.json")
    data = response.json()

    parties = {}
    candidates = {}
    for party in data["parties"]:
        parties[party["_id"]] = party["name"]
        for candidate in party["candidates"]:
            candidates[candidate["_id"]] = candidate

    polling_place = data["polling_places"][polling_place_id]
    return parties, candidates, polling_place


def fill_table_polling_place(polling_place):
    with open("src/table_polling_place.html", "r", encoding="utf-8") as file:
        table = file.read()
        table = re.sub(r"region_code", str(polling_place["region_code"]), table)
        table = re.sub(r"county_code", str(polling_place["county_code"]), table)
        table = re.sub(r"municipality_code", str(polling_place["municipality_code"]), table)
        table = re.sub(r"polling_place_code", str(polling_place["polling_place_number"]), table)
        return table


def fill_table_president(president):
    table_row = f'<tr><td style="text-align:left">{president.name}</td><td>{"áno" if president.agree else "nie"}</td></tr>'

    with open("src/table_president.html", "r", encoding="utf-8") as file:
        table = file.read()
        table = re.sub(r"table_row", table_row, table)
        return table


def fill_table_members(members):
    table_rows = []
    for member in members:
        tr = f'<tr><td style="text-align:left">{member.name}</td><td>{"áno" if member.agree else "nie"}</td></tr>'
        table_rows.append(tr)

    with open("src/table_members.html", "r", encoding="utf-8") as file:
        table = file.read()
        table = re.sub(r"table_rows", "".join(table_rows), table)
        return table


async def get_party_votes(parties, polling_place):
    pipeline = [
        {"$group" : {"_id":"$vote.party_id", "count":{"$sum":1}}},
        {"$sort":{"_id":1}}
    ]

    voted_parties = {}
    results = [result async for result in db.keys_client['gateway-db']['votes'].aggregate(pipeline)]
    for result in results:
        voted_parties[int(result["_id"])] = result["count"]

    parties_tmp = parties.copy()
    for party_id in parties_tmp:
        if party_id in voted_parties:
            votes_count = voted_parties[party_id]
        else:
            votes_count = 0

        parties_tmp[party_id] += f"\t{votes_count}"

        registered_voters_count = polling_place["registered_voters_count"]
        votes_percentage = round((votes_count / registered_voters_count) * 100, 2)
        parties_tmp[party_id] += f"\t{votes_percentage}"

    return parties_tmp

async def fill_table_parties(parties, polling_place):
    data = []
    result = await get_party_votes(parties, polling_place)
    for party_id in result:
        name, votes_count, votes_percentage = result[party_id].split("\t")
        data.append({
            "order": party_id+1,
            "name": name,
            "votes_count": votes_count,
            "votes_percentage": votes_percentage
        })

    table_rows = []
    for party in data:
        tr = f'<tr><td><div style="width: 80px">{party["order"]}</div></td><td style="text-align:left"><div style="width: 420px">{party["name"]}</div></td><td><div style="width: 75px">{party["votes_count"]}</div></td><td><div style="width: 90px">{format(float(party["votes_percentage"]), ".2f")}</div></td></tr>'
        table_rows.append(tr)

    with open("src/table_parties.html", "r", encoding="utf-8") as file:
        text = file.read()
        text = re.sub(r"table_rows", "".join(table_rows), text)
        return text


async def get_candidate_votes(parties, candidates, polling_place):
    pipeline = [
        {"$unwind": "$vote.candidate_ids"},
        {"$group" : {"_id":"$vote.candidate_ids", "count":{"$sum":1}}}
    ]

    voted_candidates = {}
    results = [result async for result in db.keys_client['gateway-db']['votes'].aggregate(pipeline)]
    for result in results:
        voted_candidates[int(result["_id"])] = result["count"]

    party_names = {}
    for candidate_id in candidates:
        candidate = candidates[candidate_id]

        if candidate_id in voted_candidates:
            candidate["votes_count"] = voted_candidates[candidate_id]
        else:
            candidate["votes_count"] = 0

        registered_voters_count = polling_place["registered_voters_count"]
        candidate_votes_percentage = round((candidate["votes_count"] / registered_voters_count) * 100, 2)
        candidate["votes_percentage"] = candidate_votes_percentage

        party_name = parties[candidates[candidate_id]["party_number"]-1]
        if party_name not in party_names:
            party_names[party_name] = [candidate]
        else:
            party_names[party_name].append(candidate)

    return party_names


def replace_header_candidates(candidates):
    table_rows = []
    for candidate in candidates:
        tr = f'<tr><td><div style="width: 80px">{candidate["order"]}</div></td><td style="text-align:left"><div style="width: 420px">{candidate["name"]}</div></td><td><div style="width: 75px">{candidate["votes_count"]}</div></td><td><div style="width: 90px">{format(candidate["votes_percentage"], ".2f")}</div></td></tr>'
        table_rows.append(tr)

    with open("src/table_candidates.html", "r", encoding="utf-8") as file:
        text = file.read()
        text = re.sub(r"table_rows", "".join(table_rows), text)
        return text


async def fill_table_candidates(parties, candidates, polling_place):
    table_candidates = ""
    result = await get_candidate_votes(parties, candidates, polling_place)
    for party_name in result:
        table_candidates += f"### {party_name}\n"

        data = []
        C = result[party_name]
        for c in C:
            candidate_name = f"{c['first_name']} {c['last_name']}"
            if len(c["degrees_before"]):
                candidate_name += f", {c['degrees_before']}"

            data.append({
                "order": c["order"],
                "name": candidate_name,
                "votes_count": c["votes_count"],
                "votes_percentage": c["votes_percentage"],
            })

        c = replace_header_candidates(data)
        table_candidates += f"{c}\n"
        # return table_candidates # delete this line when done

    return table_candidates


async def get_events():
    query = db.events_collection.find({'action': {'$in': ['elections_started', 'elections_stopped']}}, {'_id': 0}).sort('created_at', -1)
    events = [i async for i in query]
    return events


async def fill_table_events():
    events = await get_events()

    table_rows = []
    for event in events:
        tr = f'<tr><td>{"spustenie volieb" if event["action"] == "elections_started" else "ukončenie volieb"}</td><td>{event["created_at"]}</td></tr>'
        table_rows.append(tr)

    with open("src/table_events.html", "r", encoding="utf-8") as file:
        table = file.read()
        table = re.sub(r"table_rows", "".join(table_rows), table)
        return table
