<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import RoundHeader from './RoundHeader.svelte';
    // import Round from './Round.svelte';
    import type { ActiveEventData, EventData } from '$lib/types';

    $: activeData = getStore<ActiveEventData>('activeEventData');
    $: eventData = getStore<EventData>('eventData');

    $: activeRound =
        $eventData?.rounds.find((round) => round.round_number === $activeData.activeRoundNumber) ||
        $eventData?.rounds[0];

    $: roundNumbers = $eventData?.rounds.map((round) => round.round_number);

    const joincode = $page.params.joincode;
</script>

<h1>Today's Join Code: <strong>{joincode}</strong></h1>

<div class="container">
    <RoundHeader  {activeData} {activeRound} {eventData} {roundNumbers}/>
    <!-- <Round {activeRound} /> -->
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 0.75em;
        max-width: 30rem;
        margin: 5rem auto 0;
    }
</style>
