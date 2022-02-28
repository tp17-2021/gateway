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

/**
 * Election status
 */
export async function getElectionStatus() {
    try {
        let response = await axios.get(url("/../statevector/gateway/state_election.txt"))
        console.log(response.data);
        return parseInt(response.data);
    }
    catch (e) {
        console.log(e);
        return undefined;
    }
}

export async function startElection() {
    return await axios.post(url("/../voting-process-manager-api/start"))
}


export async function stopElection() {
    return axios.post(url("/../voting-process-manager-api/end"))
}

/**
 * NFC Writer
 */
export async function getWriterStatus() {
    try {
        let response = await axios.get(url("/../statevector/gateway/state_write.txt"))
        console.log(response.data);
        return parseInt(response.data);
    }
    catch (e) {
        console.log(e);
        return undefined;
    }
}

export async function startWriter() {
    return await axios.post(url("/../token-manager-api/tokens/writter/activate"))
}


export async function stopWriter() {
    return axios.post(url("/../token-manager-api/tokens/writter/deactivate"))
}

/**
 * Synchronization
 */
export async function synchronize() {
    return axios.post(url("/../synchronization-service-api/synchronize"))
}

export async function getSynchronizationStatus() {
    return axios.post(url("/../synchronization-service-api/statistics"))
}

