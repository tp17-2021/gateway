import axios from "axios";
import {gatewayConfig, gatewayConfigLoaded, jwt, report} from "../lib/stores";
import {get} from "svelte/store";
import {isDevelopmentMode} from "../lib/helpers";

export interface TVTStatus {
    name: string;
    status: "active" | "inactive";
}


jwt.subscribe((token: any) => {
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

});


export let base = (import.meta.env.VITE_BASE_PATH ?? "");

export function url(path: string) {
    // TODO: temporary solution, will call real api in the future

    // let base = "";
    // console.log("base", base);
    return `${base}${path}`;
}


export async function getElectionEvents() {
    return await axios.get(url("/../voting-process-manager-api/gateway-elections-events"));
}

export async function getVTStatuses() {
    return await axios.get(url("/../voting-process-manager-api/terminals-status"));
}

export async function getGatewayConfig() {
    return await axios.get(url("/../voting-process-manager-api/election-config"));
}

async function setStoreFromConfig(){
    try {
        let response = await getGatewayConfig()
        gatewayConfig.set(response.data);
        gatewayConfigLoaded.set(true);
    } catch (e) {
        console.error("setStoreFromConfig error, retrying in 5 seconds", e);
        setTimeout(setStoreFromConfig, 5000);
    }
}

setStoreFromConfig().then()

/**
 * Election status
 */
export async function getElectionStatus() {
    try {
        let response = await axios.get(url("/../statevector/state_election"))
        console.log(response.data);
        return parseInt(response.data);
    } catch (e) {
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

export async function startWriter() {
    console.log(url("/../token-manager-api/tokens/writter/activate"))
    return await axios.post(url("/../token-manager-api/tokens/writter/activate"))
}


export async function stopWriter() {
    return axios.post(url("/../token-manager-api/tokens/writter/deactivate"))
}

/**
 * Returns blob, use it in iframe src
 */
export async function generateReportPdf() {
    // TEST raise error
    // throw new Error("test error");

    let data = await axios.post(url("/../voting-process-manager-api/commission-paper"), {
        ...get(report)
    })

    // modified https://stackoverflow.com/questions/40674532/how-to-display-base64-encoded-pdf
    let base64 = (data.data)
    const blob = base64ToBlob(base64, 'application/pdf');
    return URL.createObjectURL(blob)

    function base64ToBlob(base64, type = "application/octet-stream") {
        const binStr = atob(base64);
        const len = binStr.length;
        const arr = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            arr[i] = binStr.charCodeAt(i);
        }
        return new Blob([arr], {type: type});
    }
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

export async function authJWTToken(password: string): Promise<boolean> {
    if (isDevelopmentMode) {
        // generate random string (example of generated mockToken: 1fggoqtjlqz643fkyhd4ao)
        let mockToken = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        jwt.set(mockToken);
        console.warn("Development mode: using mock token " + mockToken + " instead of requesting voting-process-manager-api for a real token");
        return true
    }
    let name = "admin";

    try {
        var bodyFormData = new FormData();
        bodyFormData.append('body', "");
        bodyFormData.append('username', name);
        bodyFormData.append('password', password);
        let jwr_response = await axios({
            method: "post",
            url: url("/../voting-process-manager-api/token"),
            data: bodyFormData,
            headers: {"Content-Type": "multipart/form-data"},
        })

        console.log("jwr_response", jwr_response);

        // if 200, then token is valid
        if (jwr_response.status === 200) {
            jwt.set(jwr_response.data.access_token);

            // TESTING - INVALIDATE TOKEN after 5 seconds after login
            // setTimeout(() => {
            //     jwt.set("INVALIDATED.TEST.erjgshdmfhjaesdfjhgesdjikxjfkc");
            // }, 5000);
            return true;
        } else {
            jwt.set(null);
            alert()
            return false;
        }
    } catch (e) {
        // if 401, then token is invalid (unauthorized)
        if (e.response.status === 401) {
            jwt.set(null);
        } else {
            alert("failed with error status " + e.status);
            console.log(e);
        }
        return false;
    }
}
