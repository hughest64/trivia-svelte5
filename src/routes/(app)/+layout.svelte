<script lang="ts">
    import Footer from '$lib/footer/Footer.svelte';
    import Menu from '$lib/Menu.svelte';
    import { slide } from 'svelte/transition';
    import Stores from '$lib/Stores.svelte';

    let displayMenu = false;
</script>

<Stores>
    {#if displayMenu}
        <div class="menu-slider" transition:slide={{ duration: 500 }}>
            <div class="menu-content">
                <Menu on:click={() => (displayMenu = false)} />
            </div>
            <button on:click={() => (displayMenu = false)} />
        </div>
    {/if}

    <slot />

    <footer>
        <Footer on:click={() => (displayMenu = !displayMenu)} />
    </footer>
</Stores>

<style lang="scss">
    .menu-slider {
        display: flex;
        flex-direction: column;
        position: fixed;
        top: 0;
        height: 100%;
        width: 100%;
        overflow: hidden;
        margin: 0 auto;
        z-index: 99;
        button {
            cursor: default;
            flex-grow: 1;
            width: 100%;
            padding: 0;
            background-color: transparent;
        }
    }
    .menu-content {
        justify-self: center;
        height: calc(100% - calc(var(--footer-height) + 0.5rem));
        width: 100%;
        max-width: var(--max-container-width);
        margin: 0 auto;
        border-bottom-left-radius: 3em;
        border-bottom-right-radius: 3em;
        background-color: #413f43;
    }
</style>
