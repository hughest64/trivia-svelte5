<script>
    import '$lib/styles/newstyle.scss';
</script>

<slot />

<style lang="scss">
    /* loading the font here prevents a delay in rendering the font when the page loads */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,700;1,400;1,700&display=swap');

    :global(body) {
        position: relative;
        margin: 0;
        min-height: 100vh;
    }
</style>
