<script lang="ts">
    import { enhance } from '$app/forms';
    import type { EventQuestion } from '$lib/types';

    export let roundNumber: number;
    export let question: EventQuestion;
    let questionRevealed = false;
    $: revealedText = questionRevealed ? 'Hide Question' : 'Reveal Question';

    let answerRevealed = false;
    $: answerRevealedText = answerRevealed ? 'Click To Hide Answer' : 'Click To Answer';
</script>

<div class="host-question-panel flex-column">
    <h3>{roundNumber}.{question.question_number}</h3>
    <!-- <form class="flex-column" action="?/reveal" use:enhance> -->

        <div class="switch-container-q">
            <input
                type="checkbox"
                id={`reveal-${question.question_number}`}
                name={`reveal-${question.question_number}`}
                bind:checked={questionRevealed}
            />
            <label for={`reveal-${question.question_number}`} class="switch">
                <span class="slider" class:revealed={questionRevealed} />
            </label>            
            <p>{revealedText}</p>
        </div>
        
        <!-- </form> -->
    <p>{question.text}</p>

    <!-- TODO: qustion.host_notes -->

    <!-- TODO: todo we could use the event cookie to store the stat of these, just need a form like seleting an active round -->
    <button class="button button-white" on:click={() => (answerRevealed = !answerRevealed)}>{answerRevealedText}</button>
    {#if answerRevealed}<h3>{question.answer}</h3>{/if}
</div>

<style lang="scss">
    .host-question-panel {
        padding: 1em;
    }
    
    // .switch-container {
    //     border: none;
    //     padding: 0;
    //     background-color: inherit;
    // }
</style>
