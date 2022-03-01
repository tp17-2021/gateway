<script>
	// import {config} from "../stores";
	import {url} from "@roxi/routify";
	import {onMount} from "svelte";
	import {getGatewayConfig} from "../../../api/api";

	let gatewayConfig = undefined;

	onMount(async () => {
		getGatewayConfig().then(function(config) {
			console.log(config);
			gatewayConfig = config.data;
		});
	});
</script>

<style>
	header {
		background-color: black;
		width: 100%;
	}
	.header-content {
		color: white;
		padding: 1rem;
		font-size: 24px;

		display: flex;
		place-items: center;
		width: 100%;
		max-width: 768px;

		margin: 0 auto;
	}


	img {
		margin-right: 1rem;
		margin-left: 1rem;
	}
</style>

<header>
	<div class="header-content">
		<img src="{$url('/img/sk.png')}" alt="" height="50px">
		<div>{(gatewayConfig?.texts?.elections_name_short === undefined) ? "Voľby" : gatewayConfig?.texts?.elections_name_short?.sk}</div>
	</div>
</header>

