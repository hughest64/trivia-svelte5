<script lang="ts">
    import { slide } from 'svelte/transition';
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import Round from './Round.svelte';
    import RoundSelector from './RoundSelector.svelte';
    import type { GameRound } from '$lib/types';

    const activeEventData = getStore('activeEventData');
    const playerJoined = getStore('playerJoined');
    const rounds = getStore('rounds');

    $: activeRound = $rounds.find((rd) => rd.round_number === $activeEventData.activeRoundNumber) as GameRound;
</script>

<h2>{activeRound?.title}</h2>

<RoundSelector />

{#if !$playerJoined}
    <h3 out:slide|local class="not-joined-warning">
        <form action="?/joinevent" method="post">
            <button class="submit" type="submit"><h3>Click here</h3></button>to join the game!
        </form>
    </h3>
{/if}

<Round {activeRound} />

<style lang="scss">
    .not-joined-warning {
        margin: 1rem 0;
    }
    h3 {
        font-size: 1.5rem;
    }
    form {
        display: inline;
    }
    .submit {
        text-decoration: underline;
        color: var(--color-primary);
    }
</style>
