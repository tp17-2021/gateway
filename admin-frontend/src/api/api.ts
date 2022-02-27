import axios from "axios";

export interface TVTStatus {
    name: string;
    status: "active" | "inactive";
}


// TODO: temporary solution, will call real api in the future
const base = (import.meta.env.VITE_BASE_PATH ?? "");
function url(path: string) {
    return `${base}${path}`;
}

export async function getVTStatuses(): Promise<TVTStatus[]> {
    const response = await axios.get(url("/api/vtstatuses.json"));
    return response.data.message;
}

export async function getElectionStatus() {
    return axios.get(url("/../statevector/gateway/state_election.txt"))
        .then( function (response) {
            console.log(response.data);
            return parseInt(response.data);
        }).catch(function (error) {
            return undefined;
        });
}

export async function startElection() {
    return await axios.post(url("/../voting-process-manager-api/start"))
}


export async function stopElection() {
    return axios.post(url("/../voting-process-manager-api/end"))
}

export async function synchronize() {
    return axios.post(url("/../synchronization-service-api/synchronize"))
}

export async function getSynchronizationStatus() {
    return axios.post(url("/../synchronization-service-api/statistics"))
}

