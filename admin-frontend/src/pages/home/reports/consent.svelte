<script>
    import {report} from "../../../lib/stores";
    import Button from "../../../lib/components/buttons/Button.svelte";
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
    import {goto} from "@roxi/routify";

    let objects = [$report.president, ...$report.participated_members]
    let index = -1

    let currentObject = getNextObject()

    function refreshObjects() {
        $report = $report
        objects = [$report.president, ...$report.participated_members]
    }

    function getNextObject() {
        if (index < objects.length - 1) {
            index++
            return objects[index]
        }

        // everything is consented, go to next page
        $goto("/home/reports/summary");
    }

    function getPreviousObject() {
        if (index > 0) {
            index--
            return objects[index]
        }
        else {
            // go to previous page
            $goto("/home/reports");
        }
    }

    function agree() {
        currentObject.agree = true;
        refreshObjects();
        currentObject = getNextObject()
    }

    function disagree() {
        currentObject.agree = false;
        refreshObjects();
        currentObject = getNextObject()
    }

    function back() {
        currentObject = getPreviousObject()
    }
</script>

<style lang="scss">
    h2 {
        text-align: center;
    }
</style>

<h1>Odsúhlasenie zápisnice {index+1}/{objects.length}</h1>

{#if currentObject}


<h2>{currentObject.name}</h2>
<ButtonsContainer>
    <Button on:click={agree} type="primary">Súhlas</Button>
    <Button on:click={disagree} type="error">Nesúhlas</Button>
    <Button on:click={back}>Späť</Button>
</ButtonsContainer>
{:else}
    <p>No objects exist</p>
{/if}