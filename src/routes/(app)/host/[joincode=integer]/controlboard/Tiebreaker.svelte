<script lang="ts">
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import type { LeaderboardEntry, TiebreakerRankData } from '$lib/types';

    const leaderboardEntries = getStore('leaderboard');
    const hostEntries = $leaderboardEntries?.host_leaderboard_entries || [];

    const questions = $page.data.tiebreaker_questions || [];
    const selectedQuestion = questions[0];

    const responses = getStore('tiebreakerResponses');
    $: responsesForSelectedQuestion = $responses.filter((resp) => resp.game_question_id === selectedQuestion.id) || [];

    let answerShown = false;
    $: answerButtonTxt = answerShown ? 'Hide Answer' : 'Show Answer';

    const placeMap: Record<string, string> = {
        '1': 'st',
        '2': 'nd',
        '3': 'rd'
    };

    // TODO: move to utils
    const groupEntries = (entries: LeaderboardEntry[]) => {
        // the key is the tied_for_rank, value is an array of lb entries with the same tied_for_rank
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

    let tiebreakerRankData: TiebreakerRankData[] = [];

    const handleSubmit = async (e: Event) => {
        const target = e.target as HTMLFormElement;
        const data = new FormData(target);

        const response = await fetch(target.action, {
            method: target.method,
            body: data
        });
        if (!response.ok) {
            // TODO: error handling
        }
    };
</script>

<!-- TODO: needs to be selectable (slider?) -->
<div class="tiebreaker-question-container flex-column">
    <p>{selectedQuestion.question_text}</p>
    <!-- TODO: add questions notes in here somewhere -->
    <button class="button button-secondary" on:click={() => (answerShown = !answerShown)}>
        {answerButtonTxt}
    </button>
    {#if answerShown}
        <p transition:slide>{selectedQuestion.display_answer}</p>
    {/if}
</div>

<ul class="tiebreaker-list">
    {#each Object.entries(groupedEntries) as [forRank, group]}
        <li>
            <form action="?/submit_tiebreakers" method="post" on:submit|preventDefault={handleSubmit}>
                <h3 class="spacer">For {forRank}{placeMap[forRank] || 'th'} Place</h3>

                <input type="hidden" name="tied_for_rank" value={forRank} />
                <input type="hidden" name="question_id" value={selectedQuestion.id} />
                <ul>
                    {#each group as entry}
                        {@const answer = responsesForSelectedQuestion.find((resp) => {
                            return resp.team_id === entry.team_id;
                        })}

                        <li class="input-container">
                            <span class="spacer rank-data">
                                <h3>{entry.team_name}</h3>
                                {#if answer}
                                    <!-- TODO: how to handle adding the new rank? (current rank + index, maybe?) -->
                                    <p>Grade {answer?.grade}</p>
                                {/if}
                            </span>
                            <input
                                name="team.{entry.team_id}"
                                class="tiebreaker-answer"
                                type="text"
                                placeholder="Enter Answer"
                                value={answer?.recorded_answer || ''}
                            />
                        </li>
                    {/each}
                </ul>
                <button type="submit" class="button button-primary">Apply Tiebreaker</button>
            </form>
        </li>
    {/each}
</ul>

<style lang="scss">
    .tiebreaker-question-container {
        max-width: calc(100% - 2rem);
    }
    .tiebreaker-list {
        width: calc(100% - 2rem);
        max-width: var(--max-element-width);
        margin: 0 2rem;
    }
    .spacer {
        margin: 0.75rem 0;
    }
    .rank-data {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        p {
            margin: 0;
        }
    }
</style>
