<script lang="ts">
    import { page } from '$app/stores';
    import Popup from '$lib/popup/Popup.svelte';
    import Socket from '$lib/Socket.svelte';

    const joincode = $page.params.joincode;
</script>

<svelte:head>
    <title>Trivia Mafia Event {joincode}</title>
</svelte:head>

<Socket>
    <Popup />
    <slot />
</Socket>

<style lang="scss">
    :global(main) {
        max-height: calc(100vh - 6em);
    }
</style>
