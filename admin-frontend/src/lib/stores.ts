import {writable} from "svelte/store";
import {url} from "../api/api";

export const authenticated = writable(false)
export const pin = writable("0000")
export const jwt = writable(null)
export const gatewayConfig = writable({})
export const gatewayConfigLoaded = writable(false)

export const report = writable({
    polling_place_id: 0,
    president: {
        name: "",
        agree: false,
    },
    participated_members: [],
})