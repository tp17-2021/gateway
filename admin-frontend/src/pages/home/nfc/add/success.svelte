<script>
    import ImageScreen, {icons} from "../../../../lib/ImageScreen.svelte";
    import Button from "../../../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";

    function next() {
        $goto("/home/nfc/add");
    }
</script>

<ImageScreen icon={icons.SUCCESS} title="Údaje boli úspešne nahraté
na NFC Tag">
    <Button on:click={next}>Ďalší NFC Tag</Button>
</ImageScreen>