<script lang="ts">
    import TieBreakerQuestion from './TieBreakerQuestion.svelte';
    import { deserialize } from '$app/forms';
    import { getStore } from '$lib/utils';
    import type { LeaderboardEntry, GameQuestion } from '$lib/types';
    import type { ActionResult } from '@sveltejs/kit';

    const leaderboardEntries = getStore('leaderboard');
    $: hostEntries = $leaderboardEntries?.host_leaderboard_entries || [];

    let selectedQuestion: GameQuestion;

    const responses = getStore('tiebreakerResponses');
    $: responsesForSelectedQuestion = $responses.filter((resp) => resp.game_question_id === selectedQuestion?.id) || [];

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

    const handleSubmit = async (e: Event) => {
        const target = e.target as HTMLFormElement;
        const data = new FormData(target);

        const response = await fetch(target.action, {
            method: target.method,
            body: data
        });
        const result: ActionResult = deserialize(await response.text());

        if (result.type !== 'success') {
            // TODO: handle error
        }
    };
</script>

<TieBreakerQuestion bind:selectedQuestion />

<ul class="tiebreaker-list">
    {#each Object.entries(groupedEntries) as [forRank, group]}
        <li>
            <form action="?/submit_tiebreakers" method="post" on:submit|preventDefault={handleSubmit}>
                <h3 class="spacer">For {forRank}{placeMap[forRank] || 'th'} Place</h3>

                <input type="hidden" name="tied_for_rank" value={forRank} />
                <input type="hidden" name="question_id" value={selectedQuestion?.id} />
                <ul>
                    {#each group as entry}
                        {@const answer = responsesForSelectedQuestion.find((resp) => {
                            return resp.team_id === entry.team_id;
                        })}
                        {@const inputText = answer?.recorded_answer === 'NaN' ? '-' : answer?.recorded_answer ?? ''}
                        {@const gradeValue = answer?.grade === 'NaN' ? '-' : answer?.grade || ''}

                        <li class="input-container">
                            <span class="spacer rank-data">
                                <h3>{entry.team_name}</h3>
                                {#if answer && Number(answer.round_number) <= (entry?.tiebreaker_round_number || 0)}
                                    <p>Difference {gradeValue} New Rank {entry.rank}</p>
                                {/if}
                            </span>
                            <input
                                name="team.{entry.team_id}"
                                class="tiebreaker-answer"
                                type="text"
                                placeholder="Enter Answer"
                                value={inputText}
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
