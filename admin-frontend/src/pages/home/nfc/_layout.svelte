<script lang="ts">
    import {WriterStatus, writerStatus} from "../../../api/websocket";
    import {goto} from "@roxi/routify";
    import {onDestroy, onMount} from "svelte";
    import {startWriter, stopWriter} from "../../../api/api";

    function writerStatusChanged(writerStatus): void {
        console.log("Writer status changed:", writerStatus);
        if (writerStatus === WriterStatus.OFF) {
            $goto('/home/nfc/off')
        } else if (writerStatus === WriterStatus.SUCCESS) {
            $goto("/home/nfc/success");
        } else if (writerStatus === WriterStatus.ERROR) {
            $goto("/home/nfc/error");
        }
        else if (writerStatus === WriterStatus.IDLE) {
            $goto("/home/nfc/idle");
        }
    }
    $: writerStatusChanged($writerStatus)

    onMount(() => {
        writerStatusChanged($writerStatus)

        // turn on NFC writer
        startWriter()
    })

    onDestroy(() => {
        // turn off NFC writer
        stopWriter()
    })
</script>

<slot></slot>