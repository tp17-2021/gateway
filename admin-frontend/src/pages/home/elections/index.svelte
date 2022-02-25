<script>
import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
import Button from "../../../lib/components/buttons/Button.svelte";
import {url} from "@roxi/routify";
import {startElection, stopElection} from "../../../api/api";
</script>

<h1>Voľby</h1>
<ButtonsContainer>
    <Button on:click={startElection}>Spustiť voľby</Button>
    <Button on:click={stopElection}>Ukončiť voľby</Button>
    <Button href={$url('/home/elections/pause')}>Pozastaviť voľby</Button>
</ButtonsContainer>
