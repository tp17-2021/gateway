import {writable} from "svelte/store";
import {url} from "../api/api";

export const authenticated = writable(false)
export const pin = writable("0000")
export const jwt = writable(null)
export const gatewayConfig = writable({})
export const gatewayConfigLoaded = writable(false)
export const redirectToAfterLogin = writable("/home");
redirectToAfterLogin.subscribe(url => {
    console.log("$redirectToAfterLogin", url)
})