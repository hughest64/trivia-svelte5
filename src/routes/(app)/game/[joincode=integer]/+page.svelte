<script lang="ts">
    import { page } from '$app/stores';
    import { slide } from 'svelte/transition';
    import { getStore, setEventCookie } from '$lib/utils';
    import Round from './Round.svelte';
    import RoundSelector from './RoundSelector.svelte';
    import Zeppelin from '$lib/icons/Zeppelin.svelte';
    import type { GameRound } from '$lib/types';

    const activeEventData = getStore('activeEventData');
    const currentEventData = getStore('currentEventData');
    const playerJoined = getStore('playerJoined');
    const rounds = getStore('rounds');

    $: activeRound = $rounds.find((rd) => rd.round_number === $activeEventData.activeRoundNumber) as GameRound;
    const handleGoToCurrent = () => {
        $activeEventData = {
            activeRoundNumber: $currentEventData.round_number,
            activeQuestionNumber: $currentEventData.round_number,
            activeQuestionKey: $currentEventData.question_key
        };
        setEventCookie($activeEventData, $page.params.joincode);
    };
</script>

<h2>{activeRound?.title}</h2>

{#if activeRound?.round_description}
    <p>{activeRound?.round_description}</p>
{/if}

<RoundSelector />

{#if !$playerJoined}
    <h3 out:slide|local class="not-joined-warning">
        <form action="?/joinevent" method="post">
            <button class="submit" type="submit"><h3>Click here</h3></button>to join the game!
        </form>
    </h3>
{/if}

<Round {activeRound} />

{#if $activeEventData.activeQuestionKey !== $currentEventData.question_key}
    <button class="go-to-current" transition:slide on:click={handleGoToCurrent}>
        <Zeppelin />
        <p>Jump To Current Question</p>
        <Zeppelin />
    </button>
{/if}

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
    .go-to-current {
        position: fixed;
        bottom: calc(var(--footer-height) + 0.25rem);
        z-index: 4;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1.25rem;
        background-color: var(--color-current);
        width: min(100vw, var(--max-container-width));
        text-align: center;
        font-weight: bold;
        margin: 0;
        p {
            color: var(--color-secondary);
        }
    }
</style>
