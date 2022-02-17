<!--<script>-->
<script>
    import ButtonsContainer from "../../lib/components/buttons/ButtonsContainer.svelte";
    import Button from "../../lib/components/buttons/Button.svelte";
    import {url} from "@roxi/routify";
</script>

<!--    import {url} from "@roxi/routify";-->
<!--</script>-->

<!--<h1>HOME</h1>-->
<!--<a href="{$url('/home/home2')}">Go to home 2</a>-->


<h1>Domov</h1>

<ButtonsContainer>
    <Button href={$url('/home/status')}>Stav volebných terminálov</Button>
    <Button href={$url('/home/nfc')}>Obsluha NFC tagov</Button>
    <Button href={$url('/home/elections')}>Voľby</Button>
    <Button href={$url('/home/reports')}>Zápisnica</Button>
    <Button href={$url('/home/contact')}>Kontakt</Button>
</ButtonsContainer>

