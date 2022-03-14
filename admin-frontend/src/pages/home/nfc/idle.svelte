<script>
    // TODO
    import Button from "../../../lib/components/buttons/Button.svelte";
    import ImageScreen, {icons} from "../../../lib/ImageScreen.svelte";
    import {isLoading} from "../../../lib/components/spinner/spinner";
    import {goto, url} from "@roxi/routify";
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";

    function next() {
        $isLoading = true;
        setTimeout(() => {
            $isLoading = false;
            $goto("/home/nfc/add/success");
            // goto("home/nfc/add/error");
        }, 1000);
    }

    function next2() {
        $isLoading = true;
        setTimeout(() => {
            $isLoading = false;
            // goto("home/nfc/add/success");
            $goto("/home/nfc/add/error");
        }, 1000);
    }
</script>

<ImageScreen icon={icons.INSERT_TOKEN} title="Vložte NFC Tag na čítačku">
    <ButtonsContainer>

        <Button href={$url('/home')}>Ukončiť nahrávanie</Button>
    </ButtonsContainer>
    <!--    <Button on:click={next}>[DEBUG] Zapísať na NFC tag</Button>-->
    <!--    <Button on:click={next2}>[DEBUG] Zapísať na NFC tag "s chybou"</Button>-->
</ImageScreen>