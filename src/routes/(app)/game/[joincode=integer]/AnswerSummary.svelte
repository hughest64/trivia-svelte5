<script lang="ts">
    import { getStore } from '$lib/utils';
    import HalfCredit from '$lib/leaderboards/icons/HalfCredit.svelte';
    import Correct from '$lib/leaderboards/icons/Correct.svelte';
    import Wrong from '$lib/leaderboards/icons/Wrong.svelte';
    import type { GameQuestion, Response } from '$lib/types';

    export let activeQuestion: GameQuestion;
    export let activeResponse: Response;
    $: points = activeResponse?.points_awarded || 0;

    const responseSummary = getStore('responseSummary');
    $: activeResponseSummary = $responseSummary[activeQuestion.key];

    $: totalResponses =
        (activeResponseSummary?.total || 0) + (activeResponseSummary.half || 0) + (activeResponseSummary.missing || 0);
    $: correctResponses = activeResponseSummary?.correct || 0;

    $: correct_width = correctResponses > 0 ? (correctResponses / totalResponses) * 100 : 0;
    $: wrong_width = 100 - correct_width;
</script>

<div class="answer-summary">
    <h2 class="correct-answer">{activeQuestion?.display_answer}</h2>
    {#if activeResponse?.funny}
        <p>This answer was marked as a funny answer!</p>
    {/if}

    <p><strong>You Answered:</strong></p>
    <span class="team-answer-container">
        <p class="grow">{activeResponse?.recorded_answer || '-'}</p>
        {#if points === 1}
            <Correct mt="0" width="1.5rem" height="1.5rem" />
        {:else if points === 0}
            <Wrong mt="0" width="1.5rem" height="1.5rem" />
        {:else}
            <HalfCredit mt="0" width="1.5rem" height="1.5rem" />
        {/if}
        <p class="team-points">{points} point{points === 0 ? 's' : ''}</p>
    </span>
    <p><strong>{correctResponses}/{totalResponses} Teams Received Points</strong></p>

    <span class="result-bar">
        {#if correctResponses > 0}
            <div
                class="correct"
                class:player-group={activeResponse?.points_awarded || 0 === 0}
                style:width="{correct_width}%"
            />
        {/if}
        {#if totalResponses !== correctResponses}
            <div
                class="wrong"
                class:player-group={activeResponse?.points_awarded || 0 > 0}
                style:width="{wrong_width}%"
            />
        {/if}
    </span>
</div>

<style lang="scss">
    .answer-summary {
        width: calc(100% - 2rem);
        max-width: var(--max-element-width);
        margin-bottom: 1rem;
        .correct-answer {
            text-align: center;
        }
        .team-answer-container {
            display: flex;
            align-items: center;
            .team-points {
                margin-left: 0.75rem;
            }
        }
    }

    .result-bar {
        // outline: 1px dashed purple;
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: space-between;
        // align-items: center;
        height: 2rem;
        width: 100%;
        .correct {
            outline: 1px solid var(--color-secondary);
            background-color: var(--color-current);
        }
        .wrong {
            outline: 1px solid var(--color-secondary);
            background-color: var(--color-primary);
        }
        .player-group {
            margin: 0.2rem 0;
        }
    }
</style>
