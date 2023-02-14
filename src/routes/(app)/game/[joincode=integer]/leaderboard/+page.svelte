<script lang="ts">
    import { getStore } from '$lib/utils';
    import type { PublicLeaderboard } from '$lib/types';

    $: leaderboard = getStore<PublicLeaderboard>('publicLeaderboard');
    // variable for halfaway point used to determine if a button for the user appears (go to megaround)
    $: entry = $leaderboard.leaderboard_entries[0];
</script>

<h1>Team Standings</h1>

{#if $leaderboard.through_round}
    <h3>Through Round {$leaderboard.through_round}</h3>
{/if}

<!-- existing had buttons for the host to switch between leaderboards here-->

<!-- round selector (links take you back to the game at that round) -->

<!-- TODO: each loop on the leaderboard, each li as a separate component (pass entry data to it)-->
<ul class="leaderboard-rankings">
    <!-- TODO expandable for a user's active team -->
    <li class="leaderboard-title">
        <h3 class="rank">{entry.rank}</h3>
        <h3 class="team-name">{entry.team_name}</h3>
        <h3 class="points">{entry.total_points}</h3>
    </li>
    <li class="leaderboard-title">
        <h3 class="rank">-</h3>
        <h3 class="team-name">Fake Team Name</h3>
        <h3 class="points">0</h3>
    </li>
</ul>

<!-- <pre>{JSON.stringify($leaderboard, null, 4)}</pre> -->
<style lang="scss">
    ul {
        width: 100%;
    }
    .leaderboard-title {
        display: flex;
        align-items: center;
        width: 100%;
        margin: 0.5rem 0;
        padding: 0;
        border: 2px solid var(--color-secondary);
        border-radius: 10px;
    }
    .rank {
        margin: 0;
        padding: 1rem;
        background-color: var(--color-alt-black);
        color: var(--color-tertiary);
    }
    .team-name {
        flex-grow: 1;
        padding: 0 1rem;
    }
    .points {
        padding: 0 1rem;
    }
</style>
