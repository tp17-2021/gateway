<script>
    import {report} from "../../../lib/stores";
    import {isDevelopmentMode} from "../../../lib/helpers";
</script>

<slot />

{#if isDevelopmentMode}
<pre>
    {JSON.stringify($report, null, 2)}
</pre>
{/if}
