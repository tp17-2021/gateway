<script lang="ts">
    // if jwt token is invalid, redirect to login page
    import {jwt} from "../../lib/stores";
    import {onMount} from "svelte";
    import {goto} from "@roxi/routify";

    function verifyToken(jwt) {
        console.log("jwt changed to: ", jwt);
        if (!jwt) {
            //$goto("/");
        }
    }

    onMount(() => {
        verifyToken($jwt)
    });

    $: verifyToken($jwt);


</script>

<slot></slot>
