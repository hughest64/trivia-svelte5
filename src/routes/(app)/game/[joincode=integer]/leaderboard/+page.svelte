<script lang="ts">
    import { getStore } from '$lib/utils';
    import type { PublicLeaderboard } from '$lib/types';
    import Entry from '$lib/leaderboards/Entry.svelte';

    $: leaderboard = getStore<PublicLeaderboard>('publicLeaderboard');
</script>

<h1>Team Standings</h1>

{#if $leaderboard.through_round}
    <h3>Through Round {$leaderboard.through_round}</h3>
{/if}

<!-- existing had buttons for the host to switch between leaderboards here-->

<!-- round selector (links take you back to the game at that round) -->

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
