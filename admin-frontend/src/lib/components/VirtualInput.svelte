<script lang="ts">
    import {onDestroy, onMount} from "svelte";

    export let value: string = "";
    export let id: string;
    export let domInput;
    let ignoreValueChange: boolean = false;

    let internalId;

    function valueChanged(value: string) {
        if (!domInput)
            return;
        if (ignoreValueChange) {
            return;
        }

        if (value !== domInput.value) {
            domInput.value = value;
        }
    }

    $: valueChanged(value)

    onMount(() => {
        internalId = setInterval(() => {
            // console.log("value", domInput.value);
            ignoreValueChange = true;
            value = domInput.value;
            ignoreValueChange = false;
        }, 50);
        console.log("mounted", domInput);
    });

    onDestroy(() => {
        clearInterval(internalId);
    });
</script>

<style>
    input {
        margin-bottom: 6px;
        height: 54px;
    }

</style>



<input on:keydown class="virtual-keyboard" data-kioskboard-type="keyboard" bind:this={domInput}>

<!--{JSON.stringify(value, null, 2)}-->