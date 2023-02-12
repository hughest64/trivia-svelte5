<script lang="ts">
    import Lightbox from '$lib/Lightbox.svelte';
    import { getStore } from '$lib/utils';
    import { deserialize } from '$app/forms';
    import type { GameQuestion, QuestionState } from '$lib/types';

    export let question: GameQuestion;
    let formError: string;

    $: questionStates = getStore<QuestionState[]>('questionStates') || [];
    $: questionRevealed = $questionStates.find((qs) => qs.key === question.key)?.question_displayed;
    $: hasImage = question.question_type.toLocaleLowerCase().startsWith('image');
    let displayLightbox = false;

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
            formError = result.data?.error;
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
            <input type="hidden" id={question.key} name={question.key} bind:value={questionRevealed} />
            <button class="slider" class:revealed={questionRevealed} on:click|preventDefault={handleRevealQuestion} />
        </label>
        <p>{updating ? 'Updating' : questionRevealed ? 'Hide' : 'Reveal'} Question</p>
    </div>

    <p>{question.question_text}</p>

    {#if hasImage && question?.question_url}
        {#if displayLightbox}
            <Lightbox source={question?.question_url} on:click={() => (displayLightbox = false)} />
        {/if}
        <button class="button-image" on:click={() => (displayLightbox = true)}>
            <img src={question?.question_url} alt="img round" />
        </button>
    {:else if hasImage}
        <p>Image Missing</p>
    {/if}

    {#if question.answer_notes}<p>question.answer_notes</p>{/if}

    <button class="button button-tertiary" on:click={() => (answerDisplayed = !answerDisplayed)}>
        Click To {answerDisplayed ? 'Hide' : 'Reveal'} Answer
    </button>

    {#if answerDisplayed}<h4>{question.display_answer}</h4>{/if}
</div>
