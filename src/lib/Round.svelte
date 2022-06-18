<script lang="ts">
    import type { EventRound } from '$stores/event'

    export let roundData: EventRound;
    export let currentQuestion: string | number;
    $: console.log('at round component', currentQuestion)

    // TODO: we'll pull the question from the round data via a currentQuestionIndex store value
    $: question = roundData?.questions[0] //.find(q => q.question_number === currentQuestion)
</script>

{#if roundData}
<div>
    <h3>R {roundData.round_number} Q {question?.question_number}</h3>
    <p>{question?.text}</p>
</div>
{/if}