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
            <input type="checkbox" id="all" name="all" bind:checked={allQuestionsRevealed} />
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
