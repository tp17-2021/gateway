<script lang="ts">
  export let gapSize = "default";
</script>

<style lang="scss">
  .buttons {
    display: flex;
    gap: 0px;
    flex-direction: column;
    width: 100%;
  }

  .gap-medium {
    gap: 4px;
  }

  .gap-large {
    gap: 8px;
  }

</style>
<div class="buttons gap-{gapSize}">
    <slot></slot>
</div>