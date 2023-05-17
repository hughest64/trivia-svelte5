<script>
    import '$lib/styles/app.scss';
</script>

<slot />

<style lang="scss">
    :global(body) {
        position: relative;
        margin: 0;
        min-height: 100vh;
    }
</style>
