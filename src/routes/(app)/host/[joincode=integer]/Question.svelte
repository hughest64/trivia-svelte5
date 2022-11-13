<script lang="ts">
    import { getStore } from '$lib/utils';
    import type { GameQuestion, QuestionState } from '$lib/types';

    export let question: GameQuestion;
    $: questionStates = getStore<QuestionState[]>('questionStates') || [];
    $: questionRevealed = $questionStates.find((qs) => qs.key === question.key)?.question_displayed;

    // TODO: used locally for the host, but we should respect answers being revealed to players
    // we could maybe also use the event cookie to store locally for the host
    let answerDisplayed = false;

    let updating = false;
    const handleRevealQuestion = async () => {
        if (updating) return;
        updating = true;

        // TODO: this updates locally, but it does not update the actual store, which is maybe ok?
        // to update the store we'd need to do something like:
        // questionStates.update((states) => /** make a copy, find the index, update the copy, rturn the copy*/ states );
        questionRevealed = !questionRevealed;
        const data = new FormData();
        data.set('key', question.key);
        data.set('value', questionRevealed ? 'revealed' : '');

        // const response =
        await fetch('?/reveal', { method: 'POST', body: data });
        updating = false;
    };
</script>

<div class="host-question-panel flex-column">
    <h3>{question.key}</h3>
    <div class="switch-container">
        <label for={question.key} class="switch">
            <input type="hidden" id={question.key} name={question.key} bind:value={questionRevealed} />
            <button class="slider" class:revealed={questionRevealed} on:click|preventDefault={handleRevealQuestion} />
        </label>
        <p>{updating ? 'Updating' : questionRevealed ? 'Hide' : 'Reveal'} Question</p>
    </div>

    <p>{question.question_text}</p>

    <!-- TODO: qustion.host_notes -->

    <!-- TODO: add this data to the question? or in a cookie? -->
    <button class="button button-white" on:click={() => (answerDisplayed = !answerDisplayed)}>
        Click To {answerDisplayed ? 'Hide' : 'Reveal'} Answer
    </button>

    {#if answerDisplayed}<h3>{question.display_answer}</h3>{/if}
</div>

<style lang="scss">
    .host-question-panel {
        padding: 1em;
    }
</style>
