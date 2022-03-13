<script lang="ts">
    import {onDestroy, onMount} from "svelte";
    import {getVTStatuses} from "../../api/api";
    import Panel from "../../lib/components/Panel.svelte";

    let terminalsStatuses = [];
    let interval = null;
    function terminalsStatusLoop(){
        getVTStatuses().then(function(response) {
            console.log(response);
            terminalsStatuses = response.data.terminals;
        });
    }

    onMount(async () => {
        terminalsStatusLoop();
        interval = setInterval(terminalsStatusLoop, 5000);
    });

    onDestroy(() => {
        clearInterval(interval);
    });

    function getTerminalStatusClass(status) {
        if(status === null || status === 'disconnected') {
            return 'error';
        }
        return 'success';
    }

    function getTerminalStatusLabel(status) {
        if(status === 'elections_not_started') 
            return 'Voľby nespustené';
        if(status === 'waiting_for_scan')
            return 'Čakám na tag';
        if(status === 'token_valid')
            return 'Platný token';
        if(status === 'token_not_valid')
            return 'Neplatný token';
        if(status === 'vote_success')
            return 'Úspešný hlas';
        if(status === 'vote_error')
            return 'Neúspešný hlas';
        if(status === 'disconnected')
            return 'Odpojené';
        if(status === null)
            return 'Neznámy';
        return status;
    }

</script>

<style lang="scss">
    .govuk-table {
        margin-bottom: 1rem;
        width: 100%;
        @import 'node_modules/@id-sk/frontend/govuk/components/table/_table';

        .status-success {
            color: govuk-colour("green");
        }

        .status-error {
            color: govuk-colour("red");
        }
    }
</style>

<h1>Stav volebných terminálov</h1>

<div>
    {#if terminalsStatuses.length}
        <table class="govuk-table">
            <thead class="govuk-table__head">
                <tr class="govuk-table__row">
                    <th scope="col" class="govuk-table__header">
                      <span class="th-span">
                        ID
                      </span>
                    </th>
                    <th scope="col" class="govuk-table__header">
                        <span class="th-span">
                            IP adresa
                        </span>
                    </th>
                    <th scope="col" class="govuk-table__header">
                        <span class="th-span">
                            Stav
                        </span>
                    </th>
                </tr>
            </thead>
            <tbody class="govuk-table__body">
                {#each terminalsStatuses as terminal}
                    <tr class="govuk-table__row">
                        <td class="govuk-table__cell">{terminal.id}</td>
                        <td class="govuk-table__cell">{terminal.ip_address}</td>
                        <td class="govuk-table__cell status-{getTerminalStatusClass(terminal.status)}">{getTerminalStatusLabel(terminal.status)}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    {:else}
        <Panel type="danger">Nie sú pripojené žiadne terminály.</Panel>
    {/if}
</div>
