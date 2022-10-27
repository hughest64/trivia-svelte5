<script>
    import '$lib/styles/app.scss';
</script>

<main>
    <slot />
</main>

<style lang="scss">
    /* loading the font here prevents a delay in rendering the font when the page loads */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,700;1,400;1,700&display=swap');

    :global(body) {
        margin: 0;
        min-height: 100vh;
    }
</style>
