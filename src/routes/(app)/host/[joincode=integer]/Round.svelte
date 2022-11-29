<script lang="ts">
    import Question from './Question.svelte';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import type { QuestionState, GameQuestion, GameRound } from '$lib/types';

    export let activeRound: GameRound;
    let formError: string;
    const questions: GameQuestion[] = $page.data.questions || [];

    $: roundQuestions = questions.filter((question) => question.round_number === activeRound?.round_number);
    $: questionStates = getStore<QuestionState[]>('questionStates');
    $: roundQuestionStates = $questionStates.filter((qs) => qs.round_number === activeRound?.round_number);
    $: allQuestionsRevealed = roundQuestionStates.every((q) => q.question_displayed);
    $: allQuestionsRevealedText = allQuestionsRevealed ? 'All Questions Revealed' : 'Reveal All Questions';

    let updating = false;
    const handleRevalAll = async () => {
        if (updating) return;
        updating = true;
        formError = '';

        allQuestionsRevealed = !allQuestionsRevealed;

        const data = new FormData();
        data.set('key', `${activeRound?.round_number}.all`);
        data.set('value', allQuestionsRevealed ? 'revealed' : '');

        const response = await fetch('?/reveal', { method: 'POST', body: data });
        const result = await response.json();
        if (result.type === 'invalid') {
            formError = JSON.parse(result.data)?.slice(-1)[0];
            allQuestionsRevealed = !allQuestionsRevealed;
        }
        updating = false;
    };
</script>

<div class="host-question-panel flex-column">
    <h4>{activeRound?.title}</h4>

    <p>{activeRound?.round_description}</p>

    {#if formError}<p>{formError}</p>{/if}

    <div class="switch-container">
        <label for="all" class="switch">
            <input type="hidden" id="all" name="all" bind:value={allQuestionsRevealed} />
            <button class="slider" class:revealed={allQuestionsRevealed} on:click|preventDefault={handleRevalAll} />
        </label>
        <p>{allQuestionsRevealedText}</p>
    </div>
</div>

{#each roundQuestions as question (question.question_number)}
    <Question {question} />
{/each}

<style lang="scss">
    h4 {
        margin: 2em 0.25em;
    }
</style>
