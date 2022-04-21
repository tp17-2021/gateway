<script type="ts">
    import Button from "../../../lib/components/buttons/Button.svelte";
    import {goto} from "@roxi/routify";
    import ButtonsContainer from "../../../lib/components/buttons/ButtonsContainer.svelte";
    import {report} from "../../../lib/stores";
    import Input from "../../../lib/components/Input.svelte";

    function next() {
        if (president.name === "") {
            alert("Please enter a president name");
            return;
        }
        if (members.length === 0) {
            alert("Please enter at least one member name");
            return;
        }
        $goto("/home/reports/consent");
    }

    function home() {
        $goto("/home");
    }

    let president = $report.president;
    let members = $report.participated_members;
    let newMemberName = "";

    function addMember() {
        let newMemberObject = {
            name: newMemberName,
            agree: false,
        };
        if (newMemberName !== "") {
            members = [...members, newMemberObject];
            newMemberName = "";
        }
    }

    function removeMember(index) {
        members = members.filter((_, i) => i !== index);
    }


    /**
     * Automatically update report store on change
     */
    function updateStore(president, members) {
        $report.president = president
        $report.participated_members = members.sort((a, b) => a.name.localeCompare(b.name));
    }
    $: updateStore(president, members);  // watch for changes


    function handleKeyDown(e) {
        if (e.key === "Enter") {
            addMember();
        }
    }


</script>

<style lang="scss">
  .inputContainer {
    display: grid;
    grid-template-columns: 1fr 100px;
    gap: 1rem;
    align-items: center;

    * {
      justify-self: stretch;
    }
  }

</style>

<h1>Úprava zoznamu členov</h1>
<h2>Predseda</h2>
<Input bind:value={president.name}/>

<h2>Členovia</h2>
{#each members as member, index}
    <div class="inputContainer">
        <div>{member.name}</div>
        <Button on:click={()=>removeMember(index)} type="error" size="small">✖</Button>
    </div>
{/each}

<!--<form on:submit|preventDefault={handleSubmit}>-->
    <div class="inputContainer">
        <Input bind:value={newMemberName} on:keydown={handleKeyDown} />
        <Button on:click={addMember} type="primary" >✓</Button>
    </div>
<!--</form> submit={true}-->

<ButtonsContainer>
    <Button on:click={next} type="primary">Ďalej na odsúhlasenie zápisnice</Button>
    <Button on:click={home}>Späť</Button>
</ButtonsContainer>