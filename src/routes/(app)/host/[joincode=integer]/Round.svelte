<script lang="ts">
    import Question from './Question.svelte';
    import { page } from '$app/stores';
    import type { GameRound, GameQuestion } from '$lib/types';

    export let activeRound: GameRound;
    const questions: GameQuestion[] = $page.data.questions || [];
    let allQuestionsRevealed = false;
    $: roundQuestions = questions.filter((question) => question.round_number === activeRound.round_number);
    $: allQuestionsRevealedText = allQuestionsRevealed ? 'All Questions Revealed' : 'Reveal All Questions';
</script>

<div class="host-question-panel flex-column">
    <h4>{activeRound.title}</h4>
    <p>{activeRound.round_description}</p>
    <form class="switch-container" on:submit|preventDefault>
        <label for="reveal-all-questions" class="switch">
            <input
                type="checkbox"
                id="reveal-all-questions"
                name="reveal-all-questions"
                bind:checked={allQuestionsRevealed}
                on:change={() => console.log('send msg to lock or unlock all questions for this round')}
            />
            <button type="submit" class="slider" />
        </label>
        <p>{allQuestionsRevealedText}</p>
    </form>
</div>

{#each roundQuestions as question (question.question_number)}
    <Question {question} />
{/each}

<style lang="scss">
    h4 {
        margin: 2em 0.25em;
    }
</style>
