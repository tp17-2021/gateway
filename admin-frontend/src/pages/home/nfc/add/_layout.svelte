<script lang="ts">
    import {writerStatus} from "../../../../api/websocket";
    import {goto} from "@roxi/routify";
    import {onMount} from "svelte";

    function writerStatusChanged(writerStatus): void {
        console.log("Writer status changed:", writerStatus);
        if (writerStatus === "idle") {
            $goto('/home/nfc/add')
        } else if (writerStatus === "success") {
            $goto("/home/nfc/add/success");
        } else {
            $goto("/home/nfc/add/error");
        }
    }
    $: writerStatusChanged($writerStatus)

    onMount(() => {
        writerStatusChanged($writerStatus)
    })
</script>

<slot></slot>