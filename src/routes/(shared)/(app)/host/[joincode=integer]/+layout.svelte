<script lang="ts">
    import '$lib/styles/host.scss';
    import { page } from '$app/stores';
    import Socket from '$lib/Socket.svelte';
    import NewSocket from '$lib/state/Socket.svelte';
    import Popup from '$lib/popup/Popup.svelte';
</script>

<svelte:head>
    <title>Trivia Mafia | Event {$page.params.joincode}</title>
</svelte:head>

<main class="host short">
    <Socket>
        <NewSocket />
        <Popup />
        <slot />
    </Socket>
</main>
