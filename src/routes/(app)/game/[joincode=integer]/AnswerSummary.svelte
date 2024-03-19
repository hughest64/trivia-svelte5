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
    $: totalResponses = 10; // activeResponseSummary?.total || 0;
    $: correctResponses = 6; // activeResponseSummary?.correct || 0;
    $: halfCorrectResponses = 1; //activeResponseSummary?.half || 0;

    $: correct_width = correctResponses > 0 ? (correctResponses / totalResponses) * 100 : 0;
    $: half_width = halfCorrectResponses > 0 ? (halfCorrectResponses / totalResponses) * 100 + correct_width : 0;
    const wrong_width = 100;
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
    <p><strong>{correctResponses + halfCorrectResponses}/{totalResponses} Teams Received Points</strong></p>

    <div class="resultbar" style:background-size="{correct_width}%, {half_width}%, {wrong_width}%" />
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

    .resultbar {
        height: 1.5rem;
        background-image: linear-gradient(var(--color-current), var(--color-current)),
            linear-gradient(var(--color-current), var(--color-current)),
            linear-gradient(var(--color-primary), var(--color-primary));
        background-repeat: no-repeat;
    }
</style>
