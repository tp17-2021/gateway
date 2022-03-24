<script>
import Header from "../lib/components/header/Header.svelte";
import BreadCrumb from "../lib/components/header/BreadCrumb.svelte";
import Spinner from "../lib/components/spinner/Spinner.svelte";
import {gatewayConfigLoaded, redirectToAfterLogin, jwt} from "../lib/stores";
import axios from "axios";
import {goto, url} from "@roxi/routify";
import {currentUrl} from "../lib/currentUrlStore";

// Add a 401 response interceptor
axios.interceptors.response.use((response) => response, (error) => {
    if (401 === error.response.status) {
        // save original url
        $redirectToAfterLogin = $currentUrl;
        $jwt = null;
        // redirect to login
        $goto("/");
        console.log("401 response, redirected to", $url("/"));
    } else {
        return Promise.reject(error);
    }
});

</script>

<style>
    main, .full-modal {
        flex: 1;
        display: flex;
        flex-direction: column;
        padding: 1rem;
        width: 100%;
        max-width: 768px;
        margin: 0 auto;
        box-sizing: border-box;
    }
</style>

{#if $gatewayConfigLoaded}
    <Header/>
    <main>
        <BreadCrumb />
        <Spinner />
        <slot/>
    </main>
{:else}
    <p style="text-align: center;">Načítavam</p>
{/if}