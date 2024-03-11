<script lang="ts">
    import Footer from '$lib/footer/Footer.svelte';
    import Menu from '$lib/Menu.svelte';
    import MenuDots from '$lib/icons/MenuDots.svelte';
    import { slide } from 'svelte/transition';
    import Stores from '$lib/Stores.svelte';

    let displayMenu = false;
</script>

<Stores>
    <div class="menu-button-container">
        <div class="menu-button-inner">
            <button class="menu-button" on:click={() => (displayMenu = !displayMenu)}>
                <MenuDots />
            </button>
        </div>
    </div>

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
    .menu-button-container {
        position: fixed;
        top: 0.25rem;
        display: flex;
        justify-content: center;
        width: 100%;
    }
    .menu-button-inner {
        width: min(100vw, var(--max-container-width));
        display: flex;
        justify-content: flex-end;
    }
    .menu-button {
        z-index: 99;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 50%;
        height: 2.5rem;
        width: 2.5rem;
        margin: 0;
        margin-right: 1rem;
        padding: 0;
        cursor: pointer;
        &:hover,
        &:focus {
            background-color: var(--color-current);
            outline: none;
        }
    }
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
