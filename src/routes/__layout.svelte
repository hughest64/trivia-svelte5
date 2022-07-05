<script lang="ts">
	import '$lib/styles/app.scss';
	import Footer from '$lib/Footer.svelte';
	import Menu from '$lib/Menu.svelte';
	import { fly } from 'svelte/transition';

	let displayMenu = false
</script>

<main>
	{#if displayMenu}
	<span transition:fly="{{ y: -2000, duration: 1000 }}">
		<Menu />
	</span>
	{/if}
	<slot />
</main>

<footer>
	<Footer on:click={() => displayMenu = !displayMenu} />
</footer>

<style lang="scss">
    :global(body) {
		// height: 100vh;
		margin: 0;
		:first-child {
			display: flex;
			flex-direction: column;
			min-height: 100vh;
		}
		
	}
	span {
		position: fixed;
        top: 0;
		
        // height: 10%;
        width: 100%;
        margin: 0;
        border-bottom-left-radius: 5em;
        border-bottom-right-radius: 5em;
        background-color: grey;
	}
</style>
