<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import Round from './Round.svelte';
    import type { ActiveEventData, EventData } from '$lib/types';

    $: activeData = getStore<ActiveEventData>('activeEventData');
    $: eventData = getStore<EventData>('eventData');

    $: activeRound =
        $eventData?.rounds.find((round) => round.round_number === $activeData.activeRoundNumber) ||
        $eventData?.rounds[0];

    $: roundNumbers = $eventData?.rounds.map((round) => round.round_number);

    $: joincode = $page.params?.joincode;

    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;

        $activeData = { activeQuestionNumber: 1, activeRoundNumber: Number(target.id) };

        // post to the game endpoint to set active round and question in a cookie
        await fetch('/update', {
            method: 'POST',
            body: JSON.stringify({ activeData: $activeData, joincode })
        });
    };
</script>

<h3>{activeRound.title}</h3>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        <button
            id={String(roundNum)}
            on:click={handleRoundSelect}
            class:active={$activeData.activeRoundNumber === roundNum}
            class:current={$eventData.current_round_number === roundNum}
        >
            {roundNum}
        </button>
    {/each}
</div>

<Round {activeRound} />

<style lang="scss">
    h3 {
        margin: 0.5em 0.25em;
    }
</style>
