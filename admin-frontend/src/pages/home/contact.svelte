<script>
    import {gatewayConfig} from "../../lib/stores";
</script>

<h1>Kontakt</h1>
<h2>{$gatewayConfig?.texts?.contact?.title?.sk}</h2>
<p>{$gatewayConfig?.texts?.contact?.address}</p>
<p>{$gatewayConfig?.texts?.contact?.contact_person}</p>
<p>{$gatewayConfig?.texts?.contact?.phone}</p>
<p>{$gatewayConfig?.texts?.contact?.email}</p>