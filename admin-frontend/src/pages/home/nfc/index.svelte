<script>
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
    import {url} from "@roxi/routify";
    import Button from "../../../lib/components/buttons/Button.svelte";
</script>

<h1>Obsluha NFC Tagov</h1>
<ButtonsContainer>
    <Button href={$url('/home/nfc/add')}>Nahrať údaje</Button>
    <Button href={$url('/home/nfc/delete')}>Vymazať údaje</Button>
</ButtonsContainer>