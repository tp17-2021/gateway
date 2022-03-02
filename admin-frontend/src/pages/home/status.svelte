<script lang="ts">
    import {onMount} from "svelte";
    import ButtonsContainer from "../../lib/components/buttons/ButtonsContainer.svelte";
    import {getVTStatuses, TVTStatus} from "../../api/api";
    import Panel from "../../lib/components/Panel.svelte";

    let statuses: TVTStatus[] = [];
    onMount(async () => {
        statuses = await getVTStatuses()
    });
</script>

<style lang="scss">
    .govuk-table {
        margin-bottom: 1rem;
        width: 100%;
        @import 'node_modules/@id-sk/frontend/govuk/components/table/_table';

        .status-active {
            color: govuk-colour("green");
        }

        .status-inactive {
            color: govuk-colour("red");
        }
    }
</style>

<h1>Stav volebných terminálov</h1>

<div>
    {#if statuses.length}
        <table class="govuk-table">
            <tbody class="govuk-table__body">
                {#each statuses as status}
                    <tr class="govuk-table__row">
                        <td class="govuk-table__cell">{status.name}</td>
                        <td class="govuk-table__cell status-{status.status}">{status.status}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    {:else}
        <Panel type="danger">Nie sú pripojené žiadne terminály.</Panel>
    {/if}
</div>
