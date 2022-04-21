<script>
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
    import {url} from "@roxi/routify";
    import Button from "../../../lib/components/buttons/Button.svelte";
    import Panel from "../../../lib/components/Panel.svelte";
    import {startWriter, stopWriter} from "../../../api/api";
    import {writerStatus} from "../../../api/websocket";

    // let writerStatus = undefined;


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
    }
</script>

<h1>Obsluha NFC Tagov</h1>

<div>
    <Panel anchor="writer-state" type="warning">NFC zapisovačka vypnutá. Počkajte, pokým sa zapne</Panel>
</div>

<ButtonsContainer>
    <Button type="primary" on:click={startWriterButton}>Zapnúť zapisovačku</Button>
</ButtonsContainer>
