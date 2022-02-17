<script lang="ts">
    import {onMount} from "svelte";
    import ButtonsContainer from "../../lib/components/buttons/ButtonsContainer.svelte";
    import {getVTStatuses, TVTStatus} from "../../api/api";

    let statuses: TVTStatus[] = [];
    onMount(async () => {
        statuses = await getVTStatuses()
    });
</script>

<style lang="scss">
  .status {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #ccc;

    .status-active {
      color: green;
    }

    .status-inactive {
      color: red;
    }
  }
</style>

<h1>Stav volebných terminálov</h1>
<ButtonsContainer>
    {#each statuses as status}
        <div class="status">
            <div>{status.name}</div>
            <div class="status-{status.status}">{status.status}</div>
        </div>
    {/each}
</ButtonsContainer>
