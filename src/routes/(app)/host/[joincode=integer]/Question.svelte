<script lang="ts">
    import { getStore } from '$lib/utils';
    import { deserialize } from '$app/forms';
    import type { GameQuestion, QuestionState } from '$lib/types';

    export let question: GameQuestion;
    let formError: string;

    $: questionStates = getStore<QuestionState[]>('questionStates') || [];
    $: questionRevealed = $questionStates.find((qs) => qs.key === question.key)?.question_displayed;

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

    <h3>{question.key}</h3>

    <div class="switch-container">
        <label for={question.key} class="switch">
            <input type="hidden" id={question.key} name={question.key} bind:value={questionRevealed} />
            <button class="slider" class:revealed={questionRevealed} on:click|preventDefault={handleRevealQuestion} />
        </label>
        <p>{updating ? 'Updating' : questionRevealed ? 'Hide' : 'Reveal'} Question</p>
    </div>

    <p>{question.question_text}</p>

    {#if question.answer_notes}<p>question.answer_notes</p>{/if}

    <button class="button button-tertiary" on:click={() => (answerDisplayed = !answerDisplayed)}>
        Click To {answerDisplayed ? 'Hide' : 'Reveal'} Answer
    </button>

    {#if answerDisplayed}<h3>{question.display_answer}</h3>{/if}
</div>

<style lang="scss">
    .host-question-panel {
        width: 100%;
        margin: 1em 2em;
        background-color: #e0e0e0;
        padding: 1em;
    }

    .switch-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        margin: 1em 0.5em;
        .switch {
            position: relative;
            display: inline-block;
            width: 4em;
            height: 2em;
            margin: 0 0.5em;
            .slider {
                border: none;
                padding: 0;
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
                    position: absolute;
                    content: '';
                    height: 1.75em;
                    width: 1.75em;
                    left: 0.25em;
                    bottom: 0.35em;
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
            .revealed {
                background-color: #6fcf97;
                &:before {
                    transform: translateX(2.5em);
                }
            }
        }
    }
</style>
