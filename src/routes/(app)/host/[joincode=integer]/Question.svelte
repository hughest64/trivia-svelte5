<script lang="ts">
    import type { EventQuestion } from '$lib/types';

    export let question: EventQuestion;
    let updating = false;

    $: questionRevealed = question.question_displayed;

    const handleRevealQuestion = async () => {
        if (!updating) {
            // questionRevealed = !questionRevealed;
            updating = true;
    
            const data = new FormData();
            // send and empty string for the false condition as the api will interperet that as false
            data.set('value', questionRevealed ? 'true': '');
            data.set('key', question.key);
    
            const response = await fetch('?/reveal', { method: 'POST', body: data });
            // TODO: maybe if the response is not ok, reset the question value and set an error msg?
            console.log(await response.json());
            // make sure resp.ok and
            updating = false;
        };
    };

    // TODO: add this data to the question? or in a cookie?
    let answerRevealed = false;
</script>

<div class="host-question-panel flex-column">
    <h3>{question.key}</h3>
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
