<script lang="ts">
    import { getStore, respsByround, splitQuestionKey } from '$lib/utils';
    import RoundResponses from '$lib/leaderboards/RoundResponses.svelte';
    import type { LeaderboardEntry } from '$lib/types';

    export let entry: LeaderboardEntry | undefined;

    const rounds = getStore('rounds');
    const roundStates = getStore('roundStates');
    $: isSecondHalf = Math.max(...$roundStates.map((rs) => (rs.scored ? rs.round_number : 0)));
    const teamResponseStore = getStore('responseData');
    $: groupedResps = respsByround($teamResponseStore, $rounds, $roundStates, false);
</script>

{#if entry}
    <h3>{entry.team_name}</h3>
    <div class="answer-container">
        <p class="team-password">Team Password: {entry.team_password}</p>
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
    <h3 class="error">A summary is not currently available</h3>
{/if}
