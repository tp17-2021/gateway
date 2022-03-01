<!--<script>-->
<!--    import {metatags, url} from '@roxi/routify'-->
<!--    -->
<!--    metatags.title = 'My Routify app'-->
<!--    metatags.description = 'Description coming soon...'-->
<!--</script>-->

<!--<h1>Routify Starter Template</h1>-->

<!--<p>-->
<!--    To see an example app that shows off a lot of Routify's features, go to <a href="{$url('/example')}">/example</a>-->
<!--</p>-->

<!--<p>-->
<!--    This template is ready to be used in production! just delete the example app at: src/pages/example-->
<!--</p>-->

<!--<a href="{$url('/home')}">Go to home</a>-->

<script lang="ts">
    /**
     * Pin keyboard
     * After correct pin is entered, the user is redirected to the home page
     * */


    import {onMount} from "svelte";
    import Button from "../lib/components/buttons/Button.svelte";
    import {authenticated, pin} from "../lib/stores";
    import {goto} from "@roxi/routify";
    import {authJWTToken} from "../api/api";
    // import {goto} from "$lib/navigation/goto";

    let typedPin = ""
    let error = ""
    $: pinMaxLength = $pin.length
    $: pinArray = Array.from({...typedPin.split(""), length: pinMaxLength})
    let redPin = false

    async function addToPin(value: string) {
        if (typedPin.length < pinMaxLength) {
            typedPin += value
        }

        if (typedPin.length === pinMaxLength) {
            let bearer = await authJWTToken(typedPin)
            if (bearer) {
                $authenticated = true
                console.log("correct pin")
                $goto("./home")
            } else {
                error = "Incorrect pin"
                redPin = true
            }
        }
        //
        //
        // if (typedPin === $pin) { // TODO: move to config
        //     $authenticated = true
        //     $goto("./home")
        //     console.log("correct pin")
        // } else if (typedPin.length === pinMaxLength) {
        //     redPin = true
        // }
    }

    function removeFromPin() {
        if (typedPin.length > 0) {
            typedPin = typedPin.substring(0, typedPin.length - 1)
        }
        redPin = false
    }

    onMount(async () => { // onmount is only client side
        // keyboard binding to add to pin
        // only numbers and backspace
        window.addEventListener("keydown", (event: KeyboardEvent) => {
            if (event.key.length === 1 && event.key >= "0" && event.key <= "9") {
                addToPin(event.key)
            } else if (event.key === "Backspace") {
                removeFromPin()
            } else {
                console.log("key pressed: " + event.key)
            }
        })
    })

    function clearPin() {
        typedPin = ""
        redPin = false
    }

</script>

<style lang="scss">
  .title {
    text-align: center;
    padding: .5rem 1rem;
  }


  .pinDisplay {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    margin-bottom: 10px;
    gap: 10px;

    .pinDisplay-circle {
      height: 25px;
      width: 25px;
      border-radius: 50%;
      display: inline-block;
    }

    .pinDisplay-unfilled {
      background-color: #cecece;
    }

    .pinDisplay-filled {
      background-color: black;
    }

    .pinDisplay-red {
      background-color: red !important;
    }
  }

  .pin-keyboard {
    // 4x3 grid
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(4, 1fr);
    gap: 10px;
  }

  .error {
    color: red;
    text-align: center;
    margin-top: 2rem;
  }
</style>


<!--    <span slot="subtitle">{$config.subtitle}</span>-->
<!-- pin keyboard display -->
<div class="title">Zadajte pin</div>

<div class="pinDisplay">
    {#each pinArray as pinNumber}
        {#if pinNumber === undefined}
            <div class="pinDisplay-circle pinDisplay-unfilled"></div>
        {:else}
            <div class="{redPin ? 'pinDisplay-red' : ''} pinDisplay-circle pinDisplay-filled"></div>
        {/if}
    {/each}
</div>

<!-- pin keyboard keys -->
<div class="pin-keyboard">
    <Button on:click={() => addToPin("1")}>1</Button>
    <Button on:click={() => addToPin("2")}>2</Button>
    <Button on:click={() => addToPin("3")}>3</Button>
    <Button on:click={() => addToPin("4")}>4</Button>
    <Button on:click={() => addToPin("5")}>5</Button>
    <Button on:click={() => addToPin("6")}>6</Button>
    <Button on:click={() => addToPin("7")}>7</Button>
    <Button on:click={() => addToPin("8")}>8</Button>
    <Button on:click={() => addToPin("9")}>9</Button>
    <Button on:click={() => clearPin()}>C</Button>
    <Button on:click={() => addToPin("0")}>0</Button>
    <Button on:click={() => removeFromPin()}>&lt;</Button>
</div>

{#if redPin}
    <div class="error">Zadaný PIN kód je nesprávny</div>
{/if}
