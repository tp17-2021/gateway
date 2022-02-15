<script lang="ts">
    import MainLayout from "../parts/layouts/MainLayout.svelte";
    import {navigateTo} from "svelte-router-spa";

    let pin = ""
    let pinMaxLength = 8
    $: pinArray = Array.from({...pin.split(""), length: pinMaxLength})
    let redPin = false

    function addToPin(value: string) {
        if (pin.length < pinMaxLength) {
            pin += value
        }

        if (pin === "00000000") { // TODO: move to config
            navigateTo("/gateway/auth/home")
        }
        else if (pin.length === pinMaxLength) {
            redPin = true
        }
    }

    function removeFromPin() {
        if (pin.length > 0) {
            pin = pin.substring(0, pin.length - 1)
        }
        redPin = false
    }

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

  .pin-keyboard-key {
    display: grid;
    place-items: center;
    background-color: #cecece;
    padding: 20px;
    border-bottom: 5px solid black;
  }

</style>


<MainLayout>
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
        <div class="pin-keyboard-key" on:click={()=>addToPin("1")}>1</div>
        <div class="pin-keyboard-key" on:click={()=>addToPin("2")}>2</div>
        <div class="pin-keyboard-key" on:click={()=>addToPin("3")}>3</div>
        <div class="pin-keyboard-key" on:click={()=>addToPin("4")}>4</div>
        <div class="pin-keyboard-key" on:click={()=>addToPin("5")}>5</div>
        <div class="pin-keyboard-key" on:click={()=>addToPin("6")}>6</div>
        <div class="pin-keyboard-key" on:click={()=>addToPin("7")}>7</div>
        <div class="pin-keyboard-key" on:click={()=>addToPin("8")}>8</div>
        <div class="pin-keyboard-key" on:click={()=>addToPin("9")}>9</div>
        <div></div>
        <div class="pin-keyboard-key" on:click={()=>addToPin("0")}>0</div>
        <div class="pin-keyboard-key" on:click={()=>removeFromPin()}>&lt;</div>
    </div>
</MainLayout>