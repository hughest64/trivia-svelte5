<script lang="ts">
    import { getStore } from '$lib/utils';
    import type { GameQuestion, Response } from '$lib/types';

    export let activeQuestion: GameQuestion;
    export let activeResponse: Response;
    $: points = activeResponse?.points_awarded || 0;

    const responseSummary = getStore('responseSummary');
    $: activeResponseSummary = $responseSummary[activeQuestion.key];
    $: totalResponses = activeResponseSummary?.total || 0;
    $: correctResponses = activeResponseSummary?.correct || 0;
    $: halfCorrectResponses = activeResponseSummary?.half || 0;
    $: wrongResponses = totalResponses - correctResponses - halfCorrectResponses;

    $: correct_width = correctResponses > 0 ? (correctResponses / totalResponses) * 100 : 0;
    $: half_width = halfCorrectResponses > 0 ? (halfCorrectResponses / totalResponses) * 100 + correct_width : 0;
    const wrong_width = 100;
</script>

<div class="answer-summary">
    <p>Correct Answer: <strong>{activeQuestion?.display_answer}</strong></p>
    <!-- TODO multiply by megaround vals if appropriate-->
    <p>
        You Received {points}
        {points > 0 && points <= 1 ? 'pt' : 'pts'} for this question
    </p>
    {#if activeResponse?.funny}
        <p>This answer was marked as a funny answer!</p>
    {/if}
    <p><strong>Scores of {totalResponses} team{totalResponses !== 1 ? 's' : ''}</strong></p>
    <div class="resultbar-labels">
        <p>{correctResponses}/{totalResponses}</p>
        {#if halfCorrectResponses > 0}<p>{halfCorrectResponses}/{totalResponses}</p>{/if}
        <p>{wrongResponses}/{totalResponses}</p>
    </div>

    <div class="resultbar" style:background-size="{correct_width}%, {half_width}%, {wrong_width}%" />

    <div class="resultbar-labels">
        <p>1 pt</p>
        {#if halfCorrectResponses > 0}<p>.5 pts</p>{/if}
        <p>0 pts</p>
    </div>
</div>

<style lang="scss">
    .answer-summary {
        width: calc(100% - 2rem);
        max-width: var(--max-element-width);
    }
    .resultbar {
        height: 1.5rem;
        background-image: linear-gradient(var(--color-primary), var(--color-primary)),
            linear-gradient(var(--color-secondary), var(--color-secondary)),
            linear-gradient(var(--color-disabled), var(--color-disabled));
        background-repeat: no-repeat;
    }
    .resultbar-labels {
        display: flex;
        justify-content: space-between;
        p {
            margin: 0;
            padding: 0;
        }
    }
</style>
