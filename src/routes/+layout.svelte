<script>
    import '$lib/styles/app.scss';
</script>

<main>
    <slot />
</main>

<style>
    :global(body) {
        margin: 0;
        min-height: 100vh;
    }
</style>
