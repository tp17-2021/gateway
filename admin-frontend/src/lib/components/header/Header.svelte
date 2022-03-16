<script>
	// import {config} from "../stores";
	import { url } from "@roxi/routify";
	import { onMount } from "svelte";
	import { getGatewayConfig } from "../../../api/api";

	let gatewayConfig = undefined;

	onMount(async () => {
		getGatewayConfig().then(function (config) {
			console.log(config);
			gatewayConfig = config.data;
		});
	});
</script>

<header>
	<div class="header-content">
		<img src={$url("/img/sk.png")} alt="" height="50px" />
		<div>
			{gatewayConfig?.texts?.elections_name_short === undefined
				? "Voľby"
				: gatewayConfig?.texts?.elections_name_short?.sk}
		</div>
	</div>
</header>

<style lang="scss">
	header {
		background-color: black;
		width: 100%;
		overflow: hidden;
	}

	.header-content {
		color: white;
		font-size: 24px;

		display: flex;
		place-items: center;
		width: 100%;
		max-width: 768px;

		margin: 1rem auto;

		.header-content > div {
			padding: 0 1rem;
		}
	}

	img {
		margin: 0 1rem;
	}
</style>
