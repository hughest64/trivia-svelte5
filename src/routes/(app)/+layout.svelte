<script lang="ts">
    import Footer from '$lib/footer/Footer.svelte';
    import Menu from '$lib/Menu.svelte';
    import { slide } from 'svelte/transition';
    import Stores from '$lib/Stores.svelte';

    let displayMenu = false;
</script>

{#if displayMenu}
    <div transition:slide={{ duration: 500 }}>
        <Menu on:click={() => (displayMenu = false)} />
    </div>
{/if}

<Stores>
    <slot />

    <footer>
        <Footer on:click={() => (displayMenu = !displayMenu)} />
    </footer>
</Stores>

<style lang="scss">
    div {
        position: fixed;
        top: 0;
        height: calc(100% - 5.5em);
        width: 100%;
        overflow: hidden;
        margin: 0;
        border-bottom-left-radius: 3em;
        border-bottom-right-radius: 3em;
        background-color: #413f43;
        z-index: 99;
    }
</style>
