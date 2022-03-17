<script>
import Header from "../lib/components/header/Header.svelte";
import BreadCrumb from "../lib/components/header/BreadCrumb.svelte";
import Spinner from "../lib/components/spinner/Spinner.svelte";
import { gatewayConfigLoaded } from "../lib/stores";
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
    <p>Loading</p>
{/if}