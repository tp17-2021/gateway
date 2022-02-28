<script>
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
    import {url} from "@roxi/routify";
    import Button from "../../../lib/components/buttons/Button.svelte";
    import Panel from "../../../lib/components/Panel.svelte";
    import {onDestroy, onMount} from "svelte";
    import {getWriterStatus, startWriter, stopWriter} from "../../../api/api";

    let writerStatus = undefined;

    let interval = undefined;
    onMount(async () => {
        writerStatus = await getWriterStatus();
        interval = setInterval(async () => {
            writerStatus = await getWriterStatus();
        }, 5000);
    });

    onDestroy(() => {
        clearInterval(interval);
    });



    async function startWriterButton() {
        try {
            let response = await startWriter()
            if (response.status === 200) {
                // go to idle page
                console.log("// go to idle page")
            }
        } catch (error) {
            alert(error)
        }
        writerStatus = await getWriterStatus()
    }

    async function stopWriterButton() {
        try {
            let response = await stopWriter()
            if (response.status === 200) {
                // go to idle page
                console.log("// go to idle page")
            }
        } catch (error) {
            alert(error)
        }
        writerStatus = await getWriterStatus()
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
        <Button href={$url('/home/nfc/add')}>Nahrať údaje</Button>
    {:else}
        <Button on:click={startWriterButton}>Zapnúť zapisovačku</Button>
    {/if}
</ButtonsContainer>
