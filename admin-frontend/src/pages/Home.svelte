<script lang="ts">
    import PrimaryButton from "../components/buttons/PrimaryButton.svelte";
    import {Navigate} from "svelte-router-spa";
    import MainLayout from "../parts/layouts/MainLayout.svelte";
    import Buttons from "../components/buttons/Buttons.svelte";
    import BreadCrumb from "../components/BreadCrumb.svelte";
</script>

<MainLayout>
    <BreadCrumb />
    <Buttons>
        <Navigate to="/gateway/pin">
            <PrimaryButton text="Pin"/>
        </Navigate>
        <Navigate to="/gateway/auth/home">
            <PrimaryButton text="Home (SKIP PIN)"/>
        </Navigate>
        <Navigate to="/gateway/auth/statuses">
            <PrimaryButton text="VT statuses"/>
        </Navigate>
        <Navigate to="/gateway/auth/voting">
            <PrimaryButton text="voting"/>
        </Navigate>
    </Buttons>
</MainLayout>