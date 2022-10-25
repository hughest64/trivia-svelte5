<script lang="ts">
    import type { EventRound } from '$lib/types';

    export let activeRound: EventRound;

    let allQuestionsRevealed = false;
    $: allQuestionsRevealedText = allQuestionsRevealed ? 'All Questions Revealed' : 'Reveal All Questions';
</script>

<div class="host-question-panel flex-column">
    <h4>{activeRound.title}</h4>
    <p>This should be the round description, it needs to be added to the data</p>
    <div class="switch-container">
        <label for="reveal-all-questions" class="switch">
            <input
                type="checkbox"
                id="reveal-all-questions"
                name="reveal-all-questions"
                bind:checked={allQuestionsRevealed}
            />
            <span class="slider" />
        </label>
        <p>{allQuestionsRevealedText}</p>
    </div>
</div>

<!-- {#each activeRound?.questions as question (question.question_number)}
    <h3>Question {question.question_number}</h3>
    <p>{question.text}</p>
{/each} -->
<style lang="scss">
    h4 {
        margin: 2em 0.25em;
    }
    .host-question-panel {
        width: 100%; // calc(100% - 2em);
        padding: 0;
        margin: 1em 0;
        // TODO: applies only to actual question (image rounds)
        // img {
        //     max-width: calc(100% - 2em);
        //     margin: 0.5em auto;
        // }
        // TODO: variable?
        background-color: #e0e0e0;
    }

    .switch-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        margin: 1em .5em;
        .switch {
            position: relative;
            display: inline-block;
            width: 4em;
            height: 2em;
            margin: 0 0.5em;
            input {
                opacity: 0;
                width: 0;
                height: 0;
            }
            .slider {
                position: absolute;
                cursor: pointer;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                -webkit-transition: 0.4s;
                transition: 0.4s;
                border-radius: 2em;
                background-color: #413f43;
                &:before {
                    background-color: white;
                }
                &:before {
                    position: absolute;
                    content: '';
                    height: 1.5em;
                    width: 1.5em;
                    left: 0.25em;
                    bottom: 0.25em;
                    -webkit-transition: 0.4s;
                    transition: 0.4s;
                    border-radius: 50%;
                }
            }
            input:checked + .slider {
                background-color: #6fcf97;
            }
            input:checked + .slider:before {
                transform: translateX(2em);
            }
        }
    }
</style>
