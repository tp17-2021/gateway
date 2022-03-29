<script>
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
    import Button from "../../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";
    import {generateReportPdf} from "../../../api/api";
    import {onMount} from "svelte";
    import Warning from "../../../lib/components/Warning.svelte";

    function back() {
        $goto("/home/reports/summary");
    }

    function next() {
        alert("TODO: implement send to server");
        $goto("/home/reports/pdf");
    }

    let error = false

    onMount(async () => {
        console.log("onMount");

        // fake countdown
        let timer = setInterval(() => {
            secondsRemaining--;
            if (secondsRemaining <= 0) {
                clearInterval(timer);
            }
        }, 1000);

        try {
            pdfDataBase64 = await generateReportPdf();
        } catch (e) {
            console.error(e);
            error = true;
        }

        console.log("pdf", pdfDataBase64);
    });

    let pdfDataBase64 = null;
    let secondsRemaining = 45;
</script>

<style>
    iframe {
        width: 100%;
        height: calc(100vh - 500px);
    }
</style>


{#if pdfDataBase64}
    <div>
        <iframe width='100%' height='100%' src='{pdfDataBase64}#toolbar=0&navpanes=0&scrollbar=0'></iframe>
    </div>
{:else}
    {#if error}
        <Warning>
            <h1>Chyba</h1>
            <p>
                Nastala chyba pri generovaní reportu. Stlačte tlačidlo "Späť" a skúste to znova.
            </p>
        </Warning>
    {:else}
        <Warning>
            <p>Generujem PDF...</p>
            <p>Odhadovaný čas: {secondsRemaining} sekúnd</p>
        </Warning>
    {/if}

{/if}

<ButtonsContainer>
    {#if pdfDataBase64}
        <Button on:click={next} type="primary">Odoslať na server</Button>
    {/if}
    <Button on:click={back}>Späť</Button>
</ButtonsContainer>