<script lang="ts">
    import '$lib/styles/player.scss';
    import { page } from '$app/stores';
    import Popup from '$lib/popup/Popup.svelte';
    import Socket from '$lib/Socket.svelte';

    const joincode = $page.params.joincode;
</script>

<svelte:head>
    <title>Trivia Mafia Event {joincode}</title>
</svelte:head>

<main class="short">
    <Socket>
        <Popup />
        <slot />
    </Socket>
</main>
