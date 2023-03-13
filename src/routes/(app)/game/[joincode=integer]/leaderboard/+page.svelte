<script lang="ts">
    import { getStore } from '$lib/utils';
    import Entry from '$lib/leaderboards/Entry.svelte';
    import RoundSelector from '../RoundSelector.svelte';

    const leaderboard = getStore('publicLeaderboard');
</script>

<h1>Team Standings</h1>

{#if $leaderboard.through_round}
    <h3>Through Round {$leaderboard.through_round}</h3>
{/if}

<!-- existing had buttons for the host to switch between leaderboards here-->

<RoundSelector />

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
