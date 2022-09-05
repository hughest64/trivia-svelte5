<script lang="ts">
    import { page } from '$app/stores';
    import Socket from '$lib/Socket.svelte';

    const joincode = $page.params.joincode;
</script>

<svelte:head>
    <title>Trivia Mafia Event {joincode}</title>
</svelte:head>

<Socket />

<slot />
