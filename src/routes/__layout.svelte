<script lang="ts">
	import '$lib/styles/app.scss';
	import Footer from '$lib/Footer.svelte';
</script>

<main>
	<slot />
</main>

<footer>
	<Footer />
</footer>

<style lang="scss">
    :global(body) {
		min-height: 100%;
		margin: 0;
		:first-child {
			display: flex;
			flex-direction: column;
			min-height: 100vh;
		}
		
	}
</style>
