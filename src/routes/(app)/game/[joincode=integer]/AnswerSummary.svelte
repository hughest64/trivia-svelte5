<script lang="ts">
    import { getStore } from '$lib/utils';
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
    <p>{activeResponse?.recorded_answer || '-'}</p>
    <p><strong>{correctResponses + halfCorrectResponses}/{totalResponses} Teams Received Points</strong></p>

    <div class="resultbar" style:background-size="{correct_width}%, {half_width}%, {wrong_width}%" />
</div>

<style lang="scss">
    .answer-summary {
        width: calc(100% - 2rem);
        max-width: var(--max-element-width);
        .correct-answer {
            text-align: center;
        }
    }
    .resultbar {
        height: 1.5rem;
        background-image: linear-gradient(var(--color-primary), var(--color-primary)),
            linear-gradient(var(--color-secondary), var(--color-secondary)),
            linear-gradient(var(--color-disabled), var(--color-disabled));
        background-repeat: no-repeat;
    }
</style>
