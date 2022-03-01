<script>
    import {onDestroy, onMount} from 'svelte';
import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
import Button from "../../../lib/components/buttons/Button.svelte";
import Panel from "../../../lib/components/Panel.svelte";

import {startElection, stopElection, getElectionStatus} from "../../../api/api";

let electionStatus = undefined;
let interval = undefined;

function electionStatusLoop(){
    getElectionStatus().then(function(status) {
        console.log(status);
        electionStatus = status;
    });
}

onMount(async () => {
    electionStatusLoop();
    interval = setInterval(electionStatusLoop, 5000);
});

onDestroy(() => {
    clearInterval(interval);
});

function startElectionButton() {
    startElection().then( function (response){
        let message = '';
        if(response.status === 200) {
            message += 'Úspešne spustené terminály. (' + response.data.success_terminals_count + ')\n';
            message += 'Neúspešne spustené terminály. (' + response.data.error_terminals_count + ')';
            alert(message);
        } else {
            alert(response.status)
        }
    }).catch(function (error) {
        alert(error)
    }).finally(function (){
        getElectionStatus().then(function(status) {
            electionStatus = status;
        });
    });
}

function stopElectionButton() {
    stopElection().then( function (response){
        let message = '';
        if(response.status === 200) {
            message += 'Úspešne zastavené terminály. (' + response.data.success_terminals_count + ')\n';
            message += 'Neúspešne zastavené terminály. (' + response.data.error_terminals_count + ')';
            alert(message);
        } else {
            alert(response.status)
        }
    }).catch(function (error) {
        alert(error)
    }).finally(function (){
        getElectionStatus().then(function(status) {
            electionStatus = status;
        });
    });
}

</script>


<h1>Voľby</h1>

<div>
    {#if electionStatus === 1}
        <Panel anchor="election-state" type="success">Voľby spustené.</Panel>
    {:else if electionStatus === 0}
        <Panel anchor="election-state" type="danger">Voľby nespustené.</Panel>
    {:else}
        <Panel anchor="election-state" type="warning">Stav volieb sa nepodarilo zistiť.</Panel>
    {/if}
</div>


<ButtonsContainer>
    {#if electionStatus === 1}
        <Button on:click={stopElectionButton}>Ukončiť voľby</Button>
    {:else}
        <Button on:click={startElectionButton}>Spustiť voľby</Button>
    {/if}
</ButtonsContainer>
