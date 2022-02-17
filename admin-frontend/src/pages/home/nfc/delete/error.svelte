<script>
    import ImageScreen, {icons} from "../../../../lib/ImageScreen.svelte";
    import Button from "../../../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";

    function next() {
        $goto("/home/nfc/delete/");
    }
</script>

<ImageScreen icon={icons.ERROR} title="Nepodarilo sa vymazať údaje
z NFC Tagu">
    <Button on:click={next}>Ďalší NFC Tag</Button>
</ImageScreen>