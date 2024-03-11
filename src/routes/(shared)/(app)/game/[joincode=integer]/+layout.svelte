<script lang="ts">
    import '$lib/styles/player.scss';
    import { page } from '$app/stores';
    import { setContext } from 'svelte';
    import { writable } from 'svelte/store';
    import Popup from '$lib/popup/Popup.svelte';
    import Socket from '$lib/Socket.svelte';

    const joincode = $page.params.joincode;

    // store a default swipe direction that can be used/updated in multiple components
    // it helps keep the direction in sync when clicking round buttons
    setContext('swipeDirection', writable('left'));
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
