<script lang="ts">
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import type { LeaderboardEntry } from '$lib/types';

    const leaderboardEntries = getStore('leaderboard');
    const hostEntries = $leaderboardEntries?.host_leaderboard_entries || [];

    const questions = $page.data.tiebreaker_questions || [];
    const selectedQuestion = questions[0];
    let answerShown = true;

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

<!-- TODO: needs to be selectable (slider?) -->
<div class="tiebreaker-question-container flex-column">
    <p>{selectedQuestion.question_text}</p>
    <!-- TODO: add questions notes in here somewhere -->
    <button class="button button-secondary" on:click={() => (answerShown = !answerShown)}>Show Answer</button>
    {#if answerShown}
        <p transition:slide>{selectedQuestion.display_answer}</p>
    {/if}
</div>

<ul class="tiebreaker-list">
    {#each Object.entries(groupedEntries) as [forRank, group]}
        <li>
            <h3 class="spacer">For {forRank}{placeMap[forRank] || 'th'} Place</h3>
            <ul>
                {#each group as entry}
                    <li class="input-container">
                        <h3>{entry.team_name}</h3>
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
</style>
