<script>
import {onDestroy, onMount} from 'svelte';
import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
import Button from "../../../lib/components/buttons/Button.svelte";
import {synchronize, getSynchronizationStatus} from "../../../api/api";
import dayjs from 'dayjs';

let synchronizationStatus = {
    'statistics' : {}
};

let interval = undefined;

function sychronizationStatusLoop(){
    getSynchronizationStatus().then(function(response) {
        synchronizationStatus = response.data;
    });
}

onMount(async () => {
    sychronizationStatusLoop();
    interval = setInterval(sychronizationStatusLoop, 5000);
});

onDestroy(() => {
    clearInterval(interval);
});

function synchronizeButton() {
    synchronize().then(function (response) {
        getSynchronizationStatus().then(function(response) {
            synchronizationStatus = response.data;
        });
    })
}

</script>

<style type="text/scss">
    .govuk-table {
        margin-bottom: 1rem;
        width: 100%;
        @import 'node_modules/@id-sk/frontend/govuk/components/table/_table';
    }
</style>


<h1>Synchronizácia</h1>

<div>
    <table class="govuk-table">
        <tbody class="govuk-table__body">
            <tr class="govuk-table__row">
                <th scope="row" class="govuk-table__header">Všetky hlasy</th>
                <td class="govuk-table__cell govuk-table__cell--numeric">{(synchronizationStatus.statistics?.all_count === null) ? "-" : synchronizationStatus.statistics.all_count}</td>
            </tr>
            <tr class="govuk-table__row">
                <th scope="row" class="govuk-table__header">Synchronizované</th>
                <td class="govuk-table__cell govuk-table__cell--numeric">{(synchronizationStatus.statistics?.syncronized_count === null) ? "-" : synchronizationStatus.statistics.syncronized_count}</td>
            </tr>
            <tr class="govuk-table__row">
                <th scope="row" class="govuk-table__header">Nesynchonizované</th>
                <td class="govuk-table__cell govuk-table__cell--numeric">{(synchronizationStatus.statistics?.unsyncronized_count === null) ? "-" : synchronizationStatus.statistics.unsyncronized_count}</td>
            </tr>
            <tr class="govuk-table__row">
                <th scope="row" class="govuk-table__header">Posledná synchronizácia</th>
                <td class="govuk-table__cell govuk-table__cell--numeric">
                    {#if synchronizationStatus.last_synchronization === null || synchronizationStatus.last_synchronization === undefined}
                        -
                    {:else}
                        {dayjs(synchronizationStatus.last_synchronization).format('DD.MM.YYYY HH:mm')}
                    {/if}
                </td>
            </tr>
            <tr class="govuk-table__row">
                <th scope="row" class="govuk-table__header">Posledná úspešná synchronizácia</th>
                <td class="govuk-table__cell govuk-table__cell--numeric">
                    {#if synchronizationStatus.last_success_synchronization === null || synchronizationStatus.last_success_synchronization === undefined}
                        -
                    {:else}
                        {dayjs(synchronizationStatus.last_success_synchronization).format('DD.MM.YYYY HH:mm')}
                    {/if}
                </td>
            </tr>
        </tbody>
    </table>
</div>

<ButtonsContainer>
    <Button on:click={synchronizeButton}>Synchronizovať</Button>
</ButtonsContainer>
