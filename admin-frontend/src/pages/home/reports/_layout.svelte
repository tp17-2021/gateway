<script>
    import {report} from "../../../lib/stores";
</script>

<slot />

<pre>
    {JSON.stringify($report, null, 2)}
</pre>