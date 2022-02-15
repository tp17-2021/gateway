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
        <Navigate to="/gateway/auth/voting/">
            <SecondaryButton text="Spustiť voľby"/>
        </Navigate>
        <Navigate to="/gateway/auth/voting/">
            <SecondaryButton text="Ukončiť voľby"/>
        </Navigate>
        <Navigate to="/gateway/auth/voting/">
            <SecondaryButton text="Pozastaviť voľby"/>
        </Navigate>
    </Buttons>
</MainLayout>