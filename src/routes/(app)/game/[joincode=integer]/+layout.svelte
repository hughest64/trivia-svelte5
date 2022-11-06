<script lang="ts">
    import { page } from '$app/stores';
    import Popup from '$lib/Popup.svelte';
    import Socket from '$lib/Socket.svelte';
    import { fly } from 'svelte/transition';

    const joincode = $page.params.joincode;
    let displayPopup = true;
</script>

<svelte:head>
    <title>Trivia Mafia Event {joincode}</title>
</svelte:head>

<Socket>
    {#if displayPopup}
        <div transition:fly={{ y: -2000, duration: 800 }}>
            <Popup on:click={() => (displayPopup = false)} />
        </div>
    {/if}
    <slot />
</Socket>

<style lang="scss">
    :global(main) {
        max-height: calc(100vh - 6em);
    }
    div {
        width: 100%;
    }
</style>
