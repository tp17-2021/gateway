<script lang="ts">
    export let value: any;
    export let id: string;

</script>

<style>
    input {
        margin-bottom: 6px;
        height: 54px;
    }

</style>

<input bind:value on:keydown {id}>

<!--{JSON.stringify(value, null, 2)}-->