<script lang="ts">
    import type { EventQuestion } from '$lib/types';

    export let roundNumber: number;
    export let question: EventQuestion;

    // TODO: this should be part the the question
    const questionKey = `${roundNumber}.${question.question_number}`;
    let questionRevealed = question.question_displayed;

    const handleRevealQuestion = async () => {
        questionRevealed = !questionRevealed;

        const data = new FormData();
        data.set('value', String(questionRevealed));
        data.set('key', questionKey);

        const response = await fetch('?/reveal', { method: 'POST', body: data });
        // TODO: maybe if the response is not ok, reset the question value and set an error msg? 
        console.log(response);
    };

    // TODO: add this data to the question? or in a cookie?
    let answerRevealed = false;
</script>

<div class="host-question-panel flex-column">
    <h3>{questionKey}</h3>
    <!-- TODO: can we make this a form? that would make progressive enhancement possible -->
    <div class="switch-container">
        <label for={`reveal-${question.question_number}`} class="switch">
            <input
                type="checkbox"
                id={`reveal-${question.question_number}`}
                name={`reveal-${question.question_number}`}
                checked={questionRevealed}
                on:click={handleRevealQuestion}
            />
            <span class="slider" />
        </label>
        <p>{questionRevealed ? 'Hide Question' : 'Reveal Question'}</p>
    </div>
    <p>{question.text}</p>

    <!-- TODO: qustion.host_notes -->

    <!-- TODO: todo we could use the event cookie to store the stat of these, just need a form like seleting an active round -->
    <button class="button button-white" on:click={() => (answerRevealed = !answerRevealed)}
        >{answerRevealed ? 'Click To Hide Answer' : 'Click To Answer'}</button
    >
    {#if answerRevealed}<h3>{question.answer}</h3>{/if}
</div>

<style lang="scss">
    .host-question-panel {
        padding: 1em;
    }
</style>
