<!--<script>-->
<script>
    import ButtonsContainer from "../../lib/components/buttons/ButtonsContainer.svelte";
    import Button from "../../lib/components/buttons/Button.svelte";
    import {url} from "@roxi/routify";
    import {jwt} from "../../lib/stores";

    function logout() {
        $jwt = null;
        console.log("logout", $jwt);

    }
</script>

<!--    import {url} from "@roxi/routify";-->
<!--</script>-->

<!--<h1>HOME</h1>-->
<!--<a href="{$url('/home/home2')}">Go to home 2</a>-->


<h1>Domov</h1>

<div style="margin-bottom: 4rem;">
    <ButtonsContainer gapSize="large">
        <Button size="medium" href={$url('/home/elections')}>Voľby</Button>
        <Button size="medium" href={$url('/home/nfc')}>Obsluha NFC tagov</Button>
        <Button size="medium" href={$url('/home/synchronization')}>Synchronizácia</Button>
        <Button size="medium" href={$url('/home/terminals')}>Volebné terminaly</Button>
        <Button size="medium" href={$url('/home/reports')}>Zápisnica</Button>
        <Button size="medium" href={$url('/home/contact')}>Kontakt</Button>
    </ButtonsContainer>
</div>

<ButtonsContainer>
    <Button size="medium" type="error" on:click={()=>logout()}>Odhlásiť sa</Button>
</ButtonsContainer>

