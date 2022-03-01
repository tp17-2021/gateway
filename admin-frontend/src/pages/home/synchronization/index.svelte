<script>
    import {onDestroy, onMount} from 'svelte';
import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
import Button from "../../../lib/components/buttons/Button.svelte";

import {synchronize, getSynchronizationStatus} from "../../../api/api";

let synchronizationStatus = {
    'statistics' : undefined,
};

let interval = undefined;

function sychronizationStatusLoop(){
    getSynchronizationStatus().then(function(response) {
        console.log(response);
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
        console.log(response);
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
                <td class="govuk-table__cell govuk-table__cell--numeric">{(synchronizationStatus.statistics?.all_count === undefined) ? "-" : synchronizationStatus.statistics.all_count}</td>
            </tr>
            <tr class="govuk-table__row">
                <th scope="row" class="govuk-table__header">Synchronizované</th>
                <td class="govuk-table__cell govuk-table__cell--numeric">{(synchronizationStatus.statistics?.syncronized_count === undefined) ? "-" : synchronizationStatus.statistics.syncronized_count}</td>
            </tr>
            <tr class="govuk-table__row">
                <th scope="row" class="govuk-table__header">Nesynchonizované</th>
                <td class="govuk-table__cell govuk-table__cell--numeric">{(synchronizationStatus.statistics?.unsyncronized_count === undefined) ? "-" : synchronizationStatus.statistics.unsyncronized_count}</td>
            </tr>
            <tr class="govuk-table__row">
                <th scope="row" class="govuk-table__header">Posledná synchronizácia</th>
                <td class="govuk-table__cell govuk-table__cell--numeric">{(synchronizationStatus?.last_synchronization === undefined) ? "-" : synchronizationStatus.last_synchronization}</td>
            </tr>
            <tr class="govuk-table__row">
                <th scope="row" class="govuk-table__header">Posledná úspešná synchronizácia</th>
                <td class="govuk-table__cell govuk-table__cell--numeric">{(synchronizationStatus?.last_success_synchronization === undefined) ? "-" : synchronizationStatus.last_success_synchronization}</td>
            </tr>
        </tbody>
    </table>
</div>

<ButtonsContainer>
    <Button on:click={synchronizeButton}>Synchronizovať</Button>
</ButtonsContainer>
