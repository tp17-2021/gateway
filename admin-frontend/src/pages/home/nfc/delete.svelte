<script>
    import Button from "../../../lib/components/buttons/Button.svelte";
    import ImageScreen, {icons} from "../../../lib/ImageScreen.svelte";
    import {isLoading} from "../../../lib/components/spinner/spinner";
    import {goto} from "@roxi/routify";

    // TODO
    function next() {
        $isLoading = true;
        setTimeout(() => {
            $isLoading = false;
            $goto("/home/nfc/delete/success");
            // goto("home/nfc/delete/error");
        }, 1000);
    }
    function next2() {
        $isLoading = true;
        setTimeout(() => {
            $isLoading = false;
            // goto("home/nfc/delete/success");
            $goto("/home/nfc/delete/error");
        }, 1000);
    }
</script>

<ImageScreen icon={icons.INSERT_TOKEN} title="Vložte NFC Tag na čítačku">
    <Button on:click={next}>[DEBUG] Vymazať NFC tag</Button>
    <Button on:click={next2}>[DEBUG] Vymazať NFC tag "s chybou"</Button>
</ImageScreen>