<script lang="ts">
    import { page } from '$app/stores';
    import Socket from '$lib/Socket.svelte';

    const joincode = $page.params.joincode;
</script>

<svelte:head>
    <title>Trivia Mafia Event {joincode}</title>
</svelte:head>

<Socket>
    <slot />
</Socket>

<style lang="scss">
    :global(main) {
        max-height: calc(100vh - 6em);
    }
</style>
