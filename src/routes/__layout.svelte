<script lang="ts">
	import '$lib/styles/app.scss';
	import Footer from '$lib/Footer.svelte';
	import Menu from '$lib/Menu.svelte';
	import { fly } from 'svelte/transition';

	let displayMenu = false
</script>

<main>
{#if displayMenu}
	<div transition:fly="{{ y: -2000, duration: 800 }}">
		<Menu on:click={() => displayMenu = false}/>
	</div>
{:else}
	<slot />
{/if}
</main>

<footer>
	<Footer on:click={() => displayMenu = !displayMenu} />
</footer>

<style lang="scss">
    :global(body) {
		// height: 100vh;
		margin: 0;
		// :first-child {
		// 	display: flex;
		// 	flex-direction: column;
		// 	height: 100%;
		// }
		
	}
	div {
		position: fixed;
        top: 0;
        height: calc(100% - 5.5em);
        width: 100%;
        margin: 0;
        border-bottom-left-radius: 3em;
        border-bottom-right-radius: 3em;
        background-color: #413f43;
	}
</style>
