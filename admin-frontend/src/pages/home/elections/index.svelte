<script>
    import {onDestroy, onMount} from 'svelte';
import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
import Button from "../../../lib/components/buttons/Button.svelte";
import Panel from "../../../lib/components/Panel.svelte";

import {startElection, stopElection, getElectionStatus, getElectionEvents} from "../../../api/api";
import dayjs from 'dayjs';
import 'dayjs/locale/sk';
dayjs.locale('sk')

//https://day.js.org/docs/en/display/from-now
import relativeTime from "dayjs/plugin/relativeTime";
dayjs.extend(relativeTime)


let electionStatus = undefined;
let electionEvents = [];
let interval = undefined;

function electionStatusLoop(){
    getElectionStatus().then(function(status) {
        console.log(status);
        electionStatus = status;
    });
}

function updateElectionEvents(){
    getElectionEvents().then(function(response) {
        electionEvents = response.data.events;
    });
}

function getEventLabel(event) {
        if(event === 'elections_started')
            return 'Spustenie volieb';
        if(event === 'elections_stopped')
            return 'Ukončenie volieb';
        return event;
    }

onMount(async () => {
    electionStatusLoop();
    updateElectionEvents();
    interval = setInterval(electionStatusLoop, 5000);
});

onDestroy(() => {
    clearInterval(interval);
});

function startElectionButton() {
    startElection().finally(function (){
        getElectionStatus().then(function(status) {
            electionStatus = status;
        });
        updateElectionEvents();
    });
}

function stopElectionButton() {
    stopElection().finally(function (){
        getElectionStatus().then(function(status) {
            electionStatus = status;
        });
        updateElectionEvents();
    });
}

</script>

<style lang="scss">
    .govuk-table {
        margin-bottom: 1rem;
        width: 100%;
        @import 'node_modules/@id-sk/frontend/govuk/components/table/_table';
        .govuk-table__head {
            position: sticky;
            top: 0px;
            background: white;
        }
    }

    .events-table-wrapper {
        max-height: 300px;
        overflow-y:scroll;
    }
</style>


<h1>Voľby</h1>

<div>
    {#if electionStatus === 1}
        <Panel anchor="election-state" type="success">Voľby spustené.</Panel>
    {:else if electionStatus === 0}
        <Panel anchor="election-state" type="danger">Voľby nespustené.</Panel>
    {:else}
        <Panel anchor="election-state" type="warning">Stav volieb sa nepodarilo zistiť.</Panel>
    {/if}
</div>


<ButtonsContainer>
    {#if electionStatus === 1}
        <Button on:click={stopElectionButton}>Ukončiť voľby</Button>
    {:else}
        <Button on:click={startElectionButton}>Spustiť voľby</Button>
    {/if}
</ButtonsContainer>

<div>
    {#if electionEvents.length}
        <h2>História</h2>
        <div class="events-table-wrapper">
            <table class="govuk-table" >
                <thead class="govuk-table__head">
                    <tr class="govuk-table__row">
                        <th scope="col" class="govuk-table__header">
                          <span class="th-span">
                            Udalosť
                          </span>
                        </th>
                        <th scope="col" class="govuk-table__header">
                            <span class="th-span">
                                Čas
                            </span>
                        </th>
                    </tr>
                </thead>
                <tbody class="govuk-table__body">
                    {#each electionEvents as event}
                        <tr class="govuk-table__row">
                            <td class="govuk-table__cell">{getEventLabel(event.action)}</td>
                            <td class="govuk-table__cell">
                                {#if event?.created_at}
                                    {dayjs(event.created_at).fromNow()}
                                {:else}
                                    -
                                {/if}
                             </td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
    {/if}
</div>
