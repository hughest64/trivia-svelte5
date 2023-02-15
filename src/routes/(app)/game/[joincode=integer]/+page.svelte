<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import Round from './Round.svelte';
    import RoundSelector from './RoundSelector.svelte';
    import type { ActiveEventData, GameRound } from '$lib/types';

    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: activeRound = $page.data?.rounds?.find(
        (rd) => rd.round_number === $activeEventData.activeRoundNumber
    ) as GameRound;

    // TODO: if !playerJoined create a popup w/ some options for the player to join the event or go pick a different team
</script>

<h2>{activeRound?.title}</h2>

<RoundSelector />

<Round {activeRound} />
