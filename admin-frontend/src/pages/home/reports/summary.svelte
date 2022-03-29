<script lang="ts">
    import {report} from "../../../lib/stores";
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
    import Button from "../../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";

    function back() {
        $goto("/home/reports/consent");
    }

    function next() {
        $goto("/home/reports/pdf");
    }

</script>

<style lang="scss">
    .nameAndConsent {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .success {
        color: var(--green);
    }

    .error {
        color: var(--red);
    }

</style>
<h1>Finalizácia zápisnice</h1>
<h2>Predseda</h2>
<div class="nameAndConsent">
    <div><b>{$report.president.name}</b></div>
    {#if $report.president.agree}
        <div class="success">Súhlasí</div>
    {:else}
        <div class="error">Nesúhlasí</div>
    {/if}
</div>


<h2>Členovia</h2>
{#each $report.participated_members as member}
    <hr>
    <div class="nameAndConsent">
        <div><b>{member.name}</b></div>
        {#if member.agree}
            <div class="success">Súhlasí</div>
        {:else}
            <div class="error">Nesúhlasí</div>
        {/if}
    </div>
{/each}
<hr>

<ButtonsContainer>
    <Button on:click={next} type="primary">Zobraziť PDF</Button>
    <Button on:click={back}>Späť</Button>
</ButtonsContainer>