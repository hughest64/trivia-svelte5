<script lang="ts">
    import { getStore, respsByround, splitQuestionKey } from '$lib/utils';
    import RoundResponses from '$lib/leaderboards/RoundResponses.svelte';
    import type { LeaderboardEntry } from '$lib/types';

    export let entry: LeaderboardEntry | undefined;
    console.log(entry);

    const rounds = getStore('rounds');
    const roundStates = getStore('roundStates');
    $: isSecondHalf = Math.max(...$roundStates.map((rs) => (rs.scored ? rs.round_number : 0)));
    const teamResponseStore = getStore('responseData');
    $: groupedResps = respsByround($teamResponseStore, $rounds, $roundStates, false);
</script>

{#if entry}
    <!-- TODO: make this a form and allow team name editng here -->
    <h2><strong>{entry.team_name}</strong></h2>

    <div class="answer-container">
        <p class="team-password">Team Password: {entry.team_password}</p>
        <div class="leaderboard-meta">
            <p><strong>Place:</strong> {entry.rank}</p>
            <p><strong>Points:</strong> {entry.total_points}</p>
        </div>
        <ul class="response-round-list">
            {#each groupedResps || [] as group}
                {@const isMegaRound = splitQuestionKey(group[0].key).round === String(entry.megaround)}
                <li class:megaround={isMegaRound}>
                    {#if isMegaRound}
                        <h3>Mega Round!</h3>
                    {/if}
                    <RoundResponses roundResps={group} />
                </li>
            {/each}
        </ul>
    </div>
{:else}
    <h2 class="error">A summary is not currently available</h2>
{/if}

<style lang="scss">
    .leaderboard-meta {
        display: flex;
        justify-content: space-between;
    }
</style>
