<script lang="ts">
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { getStore } from '$lib/utils';
    import type { ActiveEventData, CurrentEventData, PublicLeaderboard } from '$lib/types';
    import Entry from '$lib/leaderboards/Entry.svelte';

    $: leaderboard = getStore<PublicLeaderboard>('publicLeaderboard');

    // TODO: this is all duplicated and should be it's own component
    const roundNumbers = $page.data?.rounds?.map((rd) => rd.round_number) || [];
    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: currentEventData = getStore<CurrentEventData>('currentEventData');
    $: joincode = $page.params?.joincode;

    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;

        $activeEventData = {
            activeQuestionNumber: 1,
            activeRoundNumber: Number(target.id),
            activeQuestionKey: `${target.id}.1`
        };

        // post to the game endpoint to set active round and question in a cookie
        await fetch('/update', {
            method: 'POST',
            body: JSON.stringify({ activeEventData: $activeEventData, joincode })
        }).then(() => goto(`/game/${joincode}`));
    };
</script>

<h1>Team Standings</h1>

{#if $leaderboard.through_round}
    <h3>Through Round {$leaderboard.through_round}</h3>
{/if}

<!-- existing had buttons for the host to switch between leaderboards here-->

<div class="round-selector">
    {#each roundNumbers as roundNum}
        <button
            class:active={$activeEventData.activeRoundNumber === roundNum}
            class:current={$currentEventData.round_number === roundNum}
            id={String(roundNum)}
            on:click={handleRoundSelect}
        >
            {roundNum}
        </button>
    {/each}
</div>

<ul class="leaderboard-rankings">
    {#each $leaderboard.leaderboard_entries as entry}
        <Entry {entry} />
    {/each}
</ul>

<style lang="scss">
    ul {
        width: 100%;
    }
</style>
