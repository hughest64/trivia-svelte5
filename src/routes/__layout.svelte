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
	footer {
		position: sticky;
		bottom: 0;
		width: 100%;
		background-color: var(--color-white);
	}

    :global(body) {
			min-height: 100%;
			margin: 0;
            
		}
    :global(.content) {
        display: flex;
			flex-direction: column;
            min-height: 100vh;
    }
</style>
