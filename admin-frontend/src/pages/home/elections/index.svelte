<script>
import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
import Button from "../../../lib/components/buttons/Button.svelte";
import {url} from "@roxi/routify";
</script>

<h1>Voľby</h1>
<ButtonsContainer>
    <Button href={$url('/home/elections/start')}>Spustiť voľby</Button>
    <Button href={$url('/home/elections/stop')}>Ukončiť voľby</Button>
    <Button href={$url('/home/elections/pause')}>Pozastaviť voľby</Button>
</ButtonsContainer>