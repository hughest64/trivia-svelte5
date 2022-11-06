<script lang="ts">
    import { page } from '$app/stores';
    import Socket from '$lib/Socket.svelte';
    import Popup from '$lib/Popup.svelte';
</script>

<svelte:head>
    <title>Trivia Mafia Event {$page.params.joincode}</title>
</svelte:head>

<Socket>
    <Popup />
    <slot />
</Socket>

