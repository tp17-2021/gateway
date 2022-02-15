<script lang="ts">
    import MainLayout from "../parts/layouts/MainLayout.svelte";
    import SecondaryButton from "../components/buttons/SecondaryButton.svelte";
    import {Navigate} from "svelte-router-spa";
    import Buttons from "../components/buttons/Buttons.svelte";
</script>

<style lang="scss">

</style>


<MainLayout>
    <Buttons>
        <Navigate to="/gateway/auth/statuses">
            <SecondaryButton text="Stav volebných terminálov"/>
        </Navigate>
        <Navigate to="/gateway/auth/nfc">
            <SecondaryButton text="Obsluha NFC tagov"/>
        </Navigate>
        <Navigate to="/gateway/auth/voting">
            <SecondaryButton text="Voľby"/>
        </Navigate>
        <Navigate to="/">
            <SecondaryButton text="Zápisnica"/>
        </Navigate>
        <Navigate to="/">
            <SecondaryButton text="Kontakt"/>
        </Navigate>
    </Buttons>
</MainLayout>