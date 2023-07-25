<script lang="ts">
    import type { LeaderboardEntry } from '$lib/types';
    import { getStore } from '$lib/utils';

    const leaderboardEntries = getStore('leaderboard');
    const hostEntries = $leaderboardEntries?.host_leaderboard_entries || [];

    const placeMap: Record<string, string> = {
        '1': 'st',
        '2': 'nd',
        '3': 'rd'
    };

    const groupEntries = (entries: LeaderboardEntry[]) => {
        const groupedEntries: Record<number, LeaderboardEntry[]> = {};
        const seen = new Set();
        for (const entry of entries) {
            if (!entry.tied_for_rank) continue;

            const rank = entry.tied_for_rank;
            if (!seen.has(rank)) groupedEntries[rank] = [];

            groupedEntries[rank].push(entry);
            seen.add(rank);
        }

        return groupedEntries;
    };
    $: groupedEntries = groupEntries(hostEntries);
</script>

<ul class="tiebreaker-list">
    {#each Object.entries(groupedEntries) as [forRank, group]}
        <li>
            <h3 class="spacer">For {forRank}{placeMap[forRank] || 'th'} Place</h3>
            <ul>
                {#each group as entry}
                    <li class="tiebreaker-group-item">
                        <h3 class="spacer">{entry.team_name}</h3>
                        <input class="tiebreaker-answer" type="text" placeholder="Enter Answer" />
                    </li>
                {/each}
            </ul>
        </li>
    {/each}
</ul>

<style lang="scss">
    .tiebreaker-list {
        width: calc(100% - 2rem);
        max-width: var(--max-element-width);
        margin: 0 2rem;
    }
    .spacer {
        margin: 0.75rem 0;
    }
    .tiebreaker-group-item {
        display: flex;
        flex-direction: column;
        .tiebreaker-answer {
            width: 20rem;
            max-width: 100%;
            height: 3rem;
            padding: 1rem;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 5px;
            border: none;
            background: var(--color-question-container-bg);
            align-self: center;
        }
    }
</style>
