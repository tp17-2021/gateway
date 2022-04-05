<script lang="ts">
    import {onDestroy, onMount} from "svelte";
    import {getVTStatuses, startRegistration, stopRegistration} from "../../api/api";
    import Panel from "../../lib/components/Panel.svelte";
    import ButtonsContainer from "../../lib/components/buttons/ButtonsContainer.svelte";
    import Button from "../../lib/components/buttons/Button.svelte";
    import dayjs from 'dayjs';
    import 'dayjs/locale/sk';
    dayjs.locale('sk')

    //https://day.js.org/docs/en/display/from-now
    import relativeTime from "dayjs/plugin/relativeTime";
    dayjs.extend(relativeTime)

    let terminalsStatuses = [];
    let interval = null;
    let terminalsRegistrationStatus = undefined;

    function terminalsStatusLoop(){
        getVTStatuses().then(function(response) {
            terminalsStatuses = response.data.terminals;
            terminalsRegistrationStatus = response.data.registration_status;
        });
    }

    onMount(async () => {
        terminalsStatusLoop();
        interval = setInterval(terminalsStatusLoop, 5000);
    });

    onDestroy(() => {
        clearInterval(interval);
    });

    function startRegistrationButton() {
        startRegistration().finally(function (){
            terminalsStatusLoop();
        });
    }

    function stopRegistrationButton() {
        stopRegistration().finally(function (){
            terminalsStatusLoop();
        });
    }

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

<h1>Volebné terminály</h1>

<div>
    {#if terminalsRegistrationStatus === true }
        <Panel anchor="registration-state" type="success">Registrácia spustená.</Panel>
    {:else}
        <Panel anchor="registration-state" type="danger">Registrácia vypnutá.</Panel>
    {/if}
</div>


<ButtonsContainer>
    {#if terminalsRegistrationStatus === true }
        <Button on:click={stopRegistrationButton}>Ukončiť registráciu</Button>
    {:else}
        <Button on:click={startRegistrationButton}>Spustiť registráciu</Button>
    {/if}
</ButtonsContainer>

<div>
    <h2>Stav terminálov</h2>
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
                            Posledná aktualizácia
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
                        <td class="govuk-table__cell">
                            {#if terminal?.updated_at}
                                {dayjs(terminal.updated_at).fromNow()}
                            {:else}
                                -
                            {/if}
                         </td>
                        <td class="govuk-table__cell status-{getTerminalStatusClass(terminal.status)}">{getTerminalStatusLabel(terminal.status)}</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    {:else}
        <Panel type="danger">Nie sú pripojené žiadne terminály.</Panel>
    {/if}
</div>
