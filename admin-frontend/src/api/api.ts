import axios from "axios";
import {jwt} from "../lib/stores";

export interface TVTStatus {
    name: string;
    status: "active" | "inactive";
}


jwt.subscribe(token => {
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
});


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
        let response = await axios.get(url(base + "/../statevector/gateway/state_election.txt"))
        console.log(response.data);
        return parseInt(response.data);
    }
    catch (e) {
        console.log(e);
        return undefined;
    }
}

export async function startElection() {
    return await axios.post(url(base + "/../voting-process-manager-api/start"))
}


export async function stopElection() {
    return axios.post(url(base + "/../voting-process-manager-api/end"))
}

/**
 * NFC Writer
 */
export async function getWriterStatus() {
    try {
        let response = await axios.get(url(base + "/../statevector/gateway/state_write.txt"))
        console.log(response.data);
        return parseInt(response.data);
    }
    catch (e) {
        console.log(e);
        return undefined;
    }
}

export async function startWriter() {
    return await axios.post(url(base + "/../token-manager-api/tokens/writter/activate"))
}


export async function stopWriter() {
    return axios.post(url(base + "/../token-manager-api/tokens/writter/deactivate"))
}

/**
 * Synchronization
 */
export async function synchronize() {
    return axios.post(url(base + "/../synchronization-service-api/synchronize"))
}

export async function getSynchronizationStatus() {
    return axios.post(url(base + "/../synchronization-service-api/statistics"))
}

export async function authJWTToken(password: string):Promise<boolean> {
    let name = "admin";

    try {
        var bodyFormData = new FormData();
        bodyFormData.append('body', "");
        bodyFormData.append('username', name);
        bodyFormData.append('password', password);
        let jwr_response = await axios({
            method: "post",
            url: base + "/../voting-process-manager-api/token",
            data: bodyFormData,
            headers: { "Content-Type": "multipart/form-data" },
        })

        console.log("jwr_response", jwr_response);

        // if 200, then token is valid
        if (jwr_response.status === 200) {
            jwt.set(jwr_response.data.access_token);
            return true;
        }
        else {
            jwt.set(null);
            alert()
            return false;
        }
    }
    catch (e) {
        // if 401, then token is invalid (unauthorized)
        if (e.response.status === 401) {
            jwt.set(null);
        }
        else {
            alert("failed with error status " + e.status);
            console.log(e);
        }
        return false;
    }
}
