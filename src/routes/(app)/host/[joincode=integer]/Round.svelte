<script lang="ts">
    import Question from './Question.svelte';
    import { deserialize } from '$app/forms';
    import { getStore } from '$lib/utils';
    import type { GameRound } from '$lib/types';

    export let activeRound: GameRound;

    let error: string;
    const questions = getStore('questions');
    $: roundQuestionNumbers = $questions
        .filter((q) => q.round_number === activeRound?.round_number)
        .map((q) => q.question_number);

    $: roundQuestions = $questions.filter((question) => question.round_number === activeRound?.round_number);
    const questionStates = getStore('questionStates');
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
            error = result.data?.error as string;
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
            <button
                class="slider round"
                class:revealed={allQuestionsRevealed}
                on:click|preventDefault={handleRevalAll}
            />
        </label>
        <p>{allQuestionsRevealedText}</p>
    </div>
</div>

{#each roundQuestions as question (question.id)}
    <Question {question} />
{/each}

<!-- <style lang="scss">
    .switch {
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
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
            background-color: var(--color-secondary);
            -webkit-transition: 0.4s;
            transition: 0.4s;
            &:before {
                position: absolute;
                content: '';
                height: 26px;
                width: 26px;
                left: 4.5px;
                bottom: 4.5px;
                background-color: white;
                -webkit-transition: 0.4s;
                transition: 0.4s;
            }
            &.round {
                border-radius: 34px;
            }

            &.round:before {
                border-radius: 50%;
            }
        }
        input:checked + .slider {
            background-color: var(--color-current);
        }

        input:focus + .slider {
            box-shadow: 0 0 1px var(--color-current);
        }

        input:checked + .slider:before {
            -webkit-transform: translateX(26px);
            -ms-transform: translateX(26px);
            transform: translateX(26px);
        }
    }
</style> -->
