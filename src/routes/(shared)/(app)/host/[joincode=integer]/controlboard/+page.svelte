<script lang="ts">
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import Tiebreaker from './Tiebreaker.svelte';
    import Messaging from './Messaging.svelte';

    const params = $page.url.searchParams;
    let { tiebreaker, messaging } = Object.fromEntries(params);

    let hideTiebreaker = !tiebreaker;
    $: tiebreakerButtonText = hideTiebreaker ? 'Show Tiebreaker' : 'Hide Tiebreaker';
    let hideMessaging = !messaging;
    $: messagingButtonText = hideMessaging ? 'Message Players' : 'Hide Messages';
</script>

<h1>Control Board</h1>

<button
    class="button button-tertiary top-level"
    class:disabled={!hideTiebreaker}
    on:click={() => (hideTiebreaker = !hideTiebreaker)}
>
    {tiebreakerButtonText}
</button>
{#if !hideTiebreaker}
    <div class="tiebreaker-container flex-column" transition:slide>
        <Tiebreaker />
    </div>
{/if}

<button
    class="button button-tertiary top-level"
    class:disabled={!hideMessaging}
    on:click={() => (hideMessaging = !hideMessaging)}
>
    {messagingButtonText}
</button>
{#if !hideMessaging}
    <div class="flex-column" transition:slide>
        <Messaging />
    </div>
{/if}

<style lang="scss">
    .top-level {
        width: calc(100% - 2rem);
        text-align: right;
        padding-right: 1rem;
    }
    .tiebreaker-container {
        width: 100%;
        width: calc(100% - 2rem);
    }
</style>
