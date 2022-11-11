<script lang="ts">
    import type { GameQuestion } from '$lib/types';

    export let question: GameQuestion;
    let updating = false;

    // TODO: fix me
    $: questionRevealed = false; // question.question_displayed;
    // TODO: we need to import the questionState store
    let answerDisplayed = false;

    const handleRevealQuestion = async () => {
        if (updating) return;
        updating = true;

        questionRevealed = !questionRevealed;
        const data = new FormData();
        data.set('key', question.key);
        data.set('value', questionRevealed ? 'revealed' : '');

        // const response = 
        await fetch('?/reveal', { method: 'POST', body: data });
        // TODO: this can be local for the host, but should respect whether or not it's revealed to players
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
