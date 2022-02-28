<script>
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
    import {url} from "@roxi/routify";
    import Button from "../../../lib/components/buttons/Button.svelte";
    import Panel from "../../../lib/components/Panel.svelte";
    import {onMount} from "svelte";
    import {getWriterStatus, startWriter, stopWriter} from "../../../api/api";

    let writerStatus = undefined;

    onMount(async () => {
        getWriterStatus().then(function(status) {
            writerStatus = status;
        });
    });

    setInterval(function(){
        getWriterStatus().then(function(status) {
            writerStatus = status;
        });
    }, 5000);

    function startWriterButton() {
        startWriter().then( function (response){
            if(response.status === 200) {
                // go to idle page
            }
        }).catch(function (error) {
            alert(error)
        }).finally(function (){
            getWriterStatus().then(function(status) {
                writerStatus = status;
            });
        });
    }

    function stopWriterButton() {
        stopWriter().then( function (response){
            if(response.status === 200) {
                // go to idle page
            }
        }).catch(function (error) {
            alert(error)
        }).finally(function (){
            getWriterStatus().then(function(status) {
                writerStatus = status;
            });
        });
    }
</script>

<h1>Obsluha NFC Tagov</h1>

<div>
    {#if writerStatus === 1}
        <Panel anchor="writer-state" type="success">NFC zapisovačka zapnutá.</Panel>
    {:else }
        <Panel anchor="writer-state" type="danger">NFC zapisovačka vypnutá.</Panel>
    {/if}
</div>

<ButtonsContainer>
    {#if writerStatus === 1}
        <Button on:click={stopWriterButton}>Vypnúť zapisovačku</Button>
    {:else}
        <Button on:click={startWriterButton}>Zapnúť zapisovačku</Button>
    {/if}
</ButtonsContainer>
