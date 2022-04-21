<script lang="ts">
    export let value: any;
</script>

<style>
    input {
        margin-bottom: 6px;
        height: 54px;
    }

</style>

<input bind:value on:keydown>