<script>
    import {url} from "@roxi/routify";
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
    import Button from "../../../lib/components/buttons/Button.svelte";
</script>

<h1>Zápisnica</h1>
<ButtonsContainer>
    <Button href={$url('/home/reports/list')}>Zoznam zápisníc</Button>
    <Button href={$url('/home/reports/upload')}>Nahrať z USB</Button>
    <Button href={$url('/home/reports/download')}>Nahrať na USB</Button>
</ButtonsContainer>