<script lang="ts">
    import type { EventQuestion } from '$lib/types';

    export let question: EventQuestion;
    let questionRevealed = false;
    $: revealedText = questionRevealed ? 'Hide Question' : 'Reveal Question';
</script>

<div class="host-question-panel flex-column">
    <h3>{question.key}</h3>
    <div class="switch-container">
        <label for={`reveal-${question.question_number}`} class="switch">
            <input
                type="checkbox"
                id={`reveal-${question.question_number}`}
                name={`reveal-${question.question_number}`}
                bind:checked={questionRevealed}
            />
            <span class="slider" />
        </label>
        <p>{revealedText}</p>
    </div>
    <p>{question.text}</p>
    <!-- TODO: qustion.host_notes -->
    <!-- TODO: toggle to reveal the answer text -->
    <button class="button button-white">Click To See Answer</button>
    <!-- TODO: only show if answerRevealed -->
    <h3>{question.answer}</h3>
</div>

<style lang="scss">
    .host-question-panel {
        padding: 1em;
    }
</style>
