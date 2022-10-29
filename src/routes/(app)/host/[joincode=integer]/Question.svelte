<script lang="ts">
    import type { EventQuestion } from '$lib/types';

    export let question: EventQuestion;
    let updating = false;

    $: questionRevealed = question.question_displayed;

    const handleRevealQuestion = async () => {
        if (updating) return;
        updating = true;

        questionRevealed = !questionRevealed;
        const data = new FormData();
        data.set('key', question.key);
        data.set('value', questionRevealed ? 'revealed' : '');

        // const response = 
        await fetch('?/reveal', { method: 'POST', body: data });
        // TODO: !response is not ok reset the question value and set an error msg
        updating = false;
    };

    // TODO: add this data to the question? or in a cookie?
    let answerRevealed = false;
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

    <p>{question.text}</p>

    <!-- TODO: qustion.host_notes -->

    <button class="button button-white" on:click={() => (answerRevealed = !answerRevealed)}>
        Click To {answerRevealed ? 'Hide' : 'Reveal'} Answer
    </button>

    {#if answerRevealed}<h3>{question.answer}</h3>{/if}
</div>

<style lang="scss">
    .host-question-panel {
        padding: 1em;
    }
</style>
