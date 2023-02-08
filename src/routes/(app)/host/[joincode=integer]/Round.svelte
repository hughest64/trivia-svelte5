<script lang="ts">
    import Question from './Question.svelte';
    import { page } from '$app/stores';
    import { deserialize } from '$app/forms';
    import { getStore } from '$lib/utils';
    import type { QuestionState, GameQuestion, GameRound } from '$lib/types';

    export let activeRound: GameRound;

    let error: string;
    const questions: GameQuestion[] = $page.data.questions || [];
    $: roundQuestionNumbers = questions
        .filter((q) => q.round_number === activeRound?.round_number)
        .map((q) => q.question_number);

    $: roundQuestions = questions.filter((question) => question.round_number === activeRound?.round_number);
    $: questionStates = getStore<QuestionState[]>('questionStates');
    $: roundQuestionStates = $questionStates.filter((qs) => qs.round_number === activeRound?.round_number);

    $: allQuestionsRevealed =
        roundQuestionStates.length === roundQuestions.length && roundQuestionStates.every((q) => q.question_displayed);
    $: allQuestionsRevealedText = allQuestionsRevealed ? 'All Questions Revealed' : 'Reveal All Questions';

    let updating = false;
    const handleRevalAll = async () => {
        if (updating) return;
        updating = true;
        error = '';

        allQuestionsRevealed = !allQuestionsRevealed;

        const data = new FormData();
        data.set('round_number', String(activeRound?.round_number));
        data.set('question_numbers', JSON.stringify(roundQuestionNumbers));
        data.set('reveal', String(allQuestionsRevealed));

        const response = await fetch('?/reveal', { method: 'POST', body: data });
        const result = deserialize(await response.text());
        if (result.type === 'failure') {
            error = result.data?.error;
            allQuestionsRevealed = !allQuestionsRevealed;
        }
        updating = false;
    };
</script>

<div class="host-question-panel flex-column">
    <h2>{activeRound?.title}</h2>

    <p>{activeRound?.round_description}</p>

    {#if error}<p>{error}</p>{/if}

    <div class="switch-container">
        <label for="all" class="switch">
            <input type="hidden" id="all" name="all" bind:value={allQuestionsRevealed} />
            <button class="slider" class:revealed={allQuestionsRevealed} on:click|preventDefault={handleRevalAll} />
        </label>
        <p>{allQuestionsRevealedText}</p>
    </div>
</div>

{#each roundQuestions as question (question.id)}
    <Question {question} />
{/each}

<style lang="scss">
    .host-question-panel {
        width: 100%; // calc(100% - 2em);
        // padding: 0;
        margin: 1em 2em;
        // img {
        //     max-width: calc(100% - 2em);
        //     margin: 0.5em auto;
        // }
        background-color: #e0e0e0;
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
