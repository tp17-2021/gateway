<script lang="ts">
    export let href = "";
    export let type = "secondary";
    export let size = "small";

    export let submit: boolean = false;

    /**
     * https://idsk.gov.sk/komponenty/tlacidla
     * Text made bigger
     * removed bottom margin
     */

    if (["secondary", "primary", "error"].indexOf(type) === -1) {
        alert(
            `Button type "${type}" is not supported.`
        );
        type = "secondary";
    }
</script>

<style lang="scss">
  button {
    text-size-adjust: 100%;
    font-family: "Source Sans Pro", "Arial", sans-serif;
    -webkit-font-smoothing: antialiased;
    font-weight: 400;
    font-size: 1rem;

    box-sizing: border-box;
    display: inline-block;
    position: relative;
    width: 100%;
    margin-top: 0;
    border: 2px solid transparent;
    border-radius: 0;
    text-align: center;
    vertical-align: top;
    cursor: pointer;
    -webkit-appearance: none;
    background-color: #f3f2f1;
    box-shadow: 0 2px 0 #929191;
    color: #0b0c0c;
    padding: 15px 10px;

    //margin-bottom: 0;


  }

  .small {
    line-height: 1.1875;
  }

  .medium {
    line-height: 2.1875;
  }

  .secondary {

  }

  .primary {
    background-color: var(--green);
    color: white;
    box-shadow: 0 2px 0 #002d18;
    &:active {
      background-color: var(--green);
    }

    &:hover, &:focus {
      background-color: #204e2e;
    }
  }


  .error {
    background-color: var(--red);
    color: white;
    box-shadow: 0 2px 0 #530a06;
    &:active {
      background-color: var(--red);
    }

    &:hover, &:focus {
      background-color: #9e1912;
    }
  }

  a {
    text-decoration: none;
  }
</style>

{#if href !== ""}
    <a {href}>
        <button on:click class={type + " " + (size === "small" ? "small" : "medium")} type={submit === true ? "submit" : "button"}>
            <slot></slot>
        </button>
    </a>
{:else}
    <button on:click class={type + " " + (size === "small" ? "small" : "medium")} type={submit === true ? "submit" : "button"}>
        <slot></slot>
    </button>
{/if}