<script lang="ts">
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import type { LeaderboardEntry } from '$lib/types';

    export let entry: LeaderboardEntry;

    $: teamName = entry.team_name;

    const userStore = getStore('userData');
    const isPlayerEndpoint = $page.url.pathname.startsWith('/game');
    $: isPlayerTeamEntry = entry.team_id === $userStore.active_team_id;
    const roundStates = getStore('roundStates');
    $: isSecondHalf = Math.max(...$roundStates.map((rs) => (rs.scored ? rs.round_number : 0)));

    $: isHost = $page.url.pathname.startsWith('/host');

    // TODO: remove all instances of this and replace buttons with anchors
    const handleExpand = async (team_id: number) => {
        // TODO: temporary to maintain the host side
        if (isHost) {
            goto(`leaderboard/summary/${team_id}`, { invalidateAll: true });
        } else {
            goto('leaderboard/summary');
        }
    };
</script>

<li class="leaderboard-entry-container">
    <div class="leaderboard-entry-meta">
        <button class="rank" on:click={() => handleExpand(entry.team_id)}>
            <h3 class="rank-display">{entry.rank}</h3>
        </button>

        <div class="team-name grow">
            <button class="team-name-btn" on:click={() => handleExpand(entry.team_id)}>
                <h3 class="team-name-display">{teamName}</h3>
                {#if (isPlayerTeamEntry || !isPlayerEndpoint) && isSecondHalf && !entry.megaround}
                    <span class="megaround-alert">!Mega Round</span>
                {/if}
            </button>
        </div>

        <button class="points" on:click={() => handleExpand(entry.team_id)}>
            <h3 class="points-display">{entry.total_points}</h3>
        </button>
    </div>

    <!-- TODO: move to the summary! -->
    <!-- {#if !isPlayerEndpoint}
        <PointsAdjustment {entry} />
    {/if} -->
</li>

<style lang="scss">
    .leaderboard-entry-container {
        width: 100%;
        margin: 0.5rem 0;
        border: 2px solid var(--color-secondary);
        border-radius: 10px;
        & > * {
            display: flex;
            align-items: center;
        }
        .leaderboard-entry-meta {
            display: flex;
            width: 100%;
            padding: 0;
            margin: 0;
        }
        .rank {
            justify-content: center;
            min-width: 3.5rem;
            padding: 1.25rem;
            background-color: var(--color-alt-black);
            color: var(--color-tertiary);
        }

        .team-name {
            margin: 0.5rem 0;
            padding: 0 1rem;
            button {
                position: relative;
                text-align: left;
            }
            .team-name-btn {
                width: 100%;
            }
        }
        .points {
            padding: 1rem;
            justify-self: end;
        }

        .megaround-alert {
            font-size: 14px;
            color: var(--color-primary);
            position: absolute;
        }
    }
</style>
