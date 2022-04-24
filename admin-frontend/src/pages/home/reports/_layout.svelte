<script>
    import {report} from "../../../lib/stores";
    import {isDevelopmentMode} from "../../../lib/helpers";
    import KeyboardFiller from "../../../lib/components/KeyboardFiller.svelte";
</script>

<slot />

{#if isDevelopmentMode}
<pre>
    <!--{JSON.stringify($report, null, 2)}-->
</pre>
{/if}

<KeyboardFiller/>