<script lang="ts">
    import type { LeaderboardEntry } from '$lib/types';

    export let entry: LeaderboardEntry;
</script>

<!-- TODO expandable for a user's active team -->
<li class="leaderboard-entry-container">
    <h3 class="rank">{entry.rank}</h3>
    <h3 class="team-name">{entry.team_name}</h3>
    <h3 class="points">{entry.total_points}</h3>
</li>

<style lang="scss">
    .leaderboard-entry-container {
        display: flex;
        width: 100%;
        margin: 0.5rem 0;
        border: 2px solid var(--color-secondary);
        border-radius: 10px;
        & > * {
            display: flex;
            align-items: center;
        }
        .rank {
            justify-content: center;
            min-width: 3.5rem;
            padding: 1rem;
            background-color: var(--color-alt-black);
            color: var(--color-tertiary);
        }
        .team-name {
            flex-grow: 1;
            margin: 0.5rem 0;
            padding: 0 1rem;
        }
        .points {
            padding: 1rem;
        }
    }
</style>
