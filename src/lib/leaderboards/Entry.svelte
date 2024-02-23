<script lang="ts">
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

    // TODO: this isn't a good solution as we shouldn't revove the href (ever)
    // but we need a way to prevent players from viewing other teams entries
    $: summaryLink = isPlayerTeamEntry || isHost ? 'leaderboard/summary/' : '';
</script>

<li class="leaderboard-entry-container">
    <a
        href={`${summaryLink}${isHost ? entry.team_id : ''}`}
        class="leaderboard-entry-meta"
        class:anchor={isPlayerTeamEntry || isHost}
        data-sveltekit-reload={isHost}
    >
        <div class="rank">
            <h3 class="rank-display">{entry.rank}</h3>
        </div>

        <div class="team-name grow">
            <h3 class="team-name-display">{teamName}</h3>
            {#if (isPlayerTeamEntry || !isPlayerEndpoint) && isSecondHalf && !entry.megaround}
                <span class="megaround-alert">!Mega Round</span>
            {/if}
        </div>

        <div class="points">
            <h3 class="points-display">{entry.total_points}</h3>
        </div>
    </a>
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
            text-decoration: none;
            color: inherit;
        }
        .leaderboard-entry-meta {
            display: flex;
            width: 100%;
            padding: 0;
            margin: 0;
            cursor: default;
        }
        .anchor {
            cursor: pointer;
        }
        .rank {
            justify-content: center;
            text-align: center;
            min-width: 3.5rem;
            padding: 1.25rem;
            background-color: var(--color-alt-black);
            color: var(--color-tertiary);
        }

        .team-name {
            margin: 0.5rem 0;
            padding: 0 1rem;
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
