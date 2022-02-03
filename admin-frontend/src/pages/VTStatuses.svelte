<script lang="ts">
    import MainLayout from "../parts/layouts/MainLayout.svelte";
    import SecondaryButton from "../components/buttons/SecondaryButton.svelte";
    import {Navigate} from "svelte-router-spa";
    import Buttons from "../components/buttons/Buttons.svelte";

    let statuses = [
        {name: "ID01", status: "active"},
        {name: "ID02", status: "active"},
        {name: "ID03", status: "inactive"},
        {name: "ID04", status: "inactive"},
        {name: "ID05", status: "inactive"},
        {name: "ID06", status: "inactive"},
        {name: "ID07", status: "inactive"},
    ]
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


<MainLayout>
    <Buttons>
        {#each statuses as status}
            <div class="status">
                <div>{status.name}</div>
                <div class="status-{status.status}">{status.status}</div>
            </div>
        {/each}
        <hr>
    </Buttons>
</MainLayout>