import {writable} from "svelte/store";

export const loggedIn = writable(false);
export const config = writable({});
export const debugEnabled = writable(false);
export const configIsLoading = writable(false);