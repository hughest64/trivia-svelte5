<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import { deserialize } from '$app/forms';
    import type { GameQuestion } from '$lib/types';

    const joincode = $page.params.joincode;

    export let question: GameQuestion;
    let formError: string;

    const roundStates = getStore('roundStates');
    $: roundIsLocked = $roundStates.find((rs) => rs.round_number === question.round_number)?.locked;
    const responses = getStore('responseData');

    $: respSummary = (() => {
        const questionResponses = $responses.filter((r) => r.key === question.key);
        const correct = questionResponses.filter((r) => r.points_awarded === 1).length;
        const half = questionResponses.filter((r) => r.points_awarded === 0.5).length;
        const funny = questionResponses.filter((r) => r.funny).map((r) => r.recorded_answer);
        return { total: questionResponses.length, correct, half, funny };
    })();

    const questionStates = getStore('questionStates') || [];
    $: questionRevealed = $questionStates.find((qs) => qs.key === question.key)?.question_displayed;
    $: hasImage = question.question_type.toLocaleLowerCase().startsWith('image');
    $: hasSoundLink = question.question_type.toLocaleLowerCase().startsWith('sound');

    // TODO: default should be set based on whether or not answers are revealed for all
    let answerDisplayed = false;

    let updating = false;
    const handleRevealQuestion = async () => {
        if (updating) return;
        updating = true;
        formError = '';

        // update the state locally only, the store value is updated from the web socket response
        questionRevealed = !questionRevealed;
        const data = new FormData();
        data.set('round_number', String(question.round_number));
        // stringify an array of a single question number for compatibility with reveal all
        data.set('question_numbers', JSON.stringify([question.question_number]));
        data.set('reveal', String(questionRevealed));

        const response = await fetch('?/reveal', { method: 'POST', body: data });
        const result = deserialize(await response.text());
        if (result.type === 'failure') {
            formError = result.data?.error as string;
            questionRevealed = !questionRevealed;
        }
        updating = false;
    };
</script>

<div class="host-question-panel flex-column">
    {#if formError}<p>{formError}</p>{/if}

    <h4 class="question-key">{question.key}</h4>

    <div class="switch-container">
        <label for={question.key} class="switch">
            <input type="checkbox" id={question.key} name={question.key} bind:checked={questionRevealed} />
            <button
                class="slider round"
                class:revealed={questionRevealed}
                on:click|preventDefault={handleRevealQuestion}
            />
        </label>
        <!-- TODO: keep the updating logic? <p>{updating ? 'Updating' : questionRevealed ? 'Hide' : 'Reveal'} Question</p> -->
        <p>{questionRevealed ? 'Hide' : 'Reveal'} Question</p>
    </div>

    <p>{question.question_text}</p>

    <!-- Image Round -->
    {#if hasImage && question?.question_url}
        <a href="/host/{joincode}/img?key={question.key}" class="button-image">
            <img src={question?.question_url} alt="img round" />
        </a>
    {:else if hasImage}
        <p>Image Missing</p>
    {/if}

    <!-- Sound Round -->
    {#if hasSoundLink && question?.question_url}
        <a href={question.question_url} rel="external" target="_blank">Link to sound file</a>
    {:else if hasSoundLink}
        <p>Sound Link Missing</p>
    {/if}

    {#if question.question_notes}<p><strong>Notes:</strong> {question.question_notes}</p>{/if}

    <button class="button button-tertiary" on:click={() => (answerDisplayed = !answerDisplayed)}>
        Click To {answerDisplayed ? 'Hide' : 'Reveal'} Answer
    </button>

    {#if answerDisplayed}
        <h4>{question.display_answer}</h4>
        {#if question.answer_notes}<p><strong>Notes:</strong> {question.answer_notes}</p>{/if}

        {#if respSummary.total > 0 && roundIsLocked}
            <p class="resp-summary">
                {respSummary.correct}/{respSummary.total} correct, {respSummary.half} half points
            </p>
        {/if}
        {#if respSummary.funny.length > 0 && roundIsLocked}
            <p>Funny Responses: {respSummary.funny.join(', ')}</p>
        {/if}
    {/if}
</div>

<style lang="scss">
    .resp-summary {
        color: var(--color-primary);
    }
</style>
