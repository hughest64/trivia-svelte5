<script lang="ts">
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

</script>

<RoundHeader  {activeData} {activeRound} {eventData} {roundNumbers}/>
<!-- <Round {activeRound} /> -->
