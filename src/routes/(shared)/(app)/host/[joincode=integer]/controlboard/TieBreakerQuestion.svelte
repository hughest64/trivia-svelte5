<script lang="ts">
    import { page } from '$app/stores';
    import { slide } from 'svelte/transition';
    import DoubleArrow from '$lib/icons/DoubleArrow.svelte';

    const tbquestions = $page.data.tiebreaker_questions || [];
    export let selectedQuestion = tbquestions[0];
    $: selectedQuestionIndex = tbquestions.findIndex((q) => q.id === selectedQuestion?.id);

    let answerShown = false;
    $: answerButtonTxt = answerShown ? 'Hide Answer' : 'Show Answer';

    const handleQuestionSelect = async (event: MouseEvent | CustomEvent | KeyboardEvent) => {
        const keyCode = (event as KeyboardEvent).code;
        // SVG elements are tricksy when handling on clicks
        const buttonDirection = (event.target as HTMLElement).closest('button')?.id;

        let nextQuestionIndex = selectedQuestionIndex;
        if (buttonDirection === 'left' || keyCode === 'ArrowLeft') {
            nextQuestionIndex -= 1;
        } else if (buttonDirection === 'right' || keyCode === 'ArrowRight') {
            nextQuestionIndex += 1;
        }
        const nextQuestion = tbquestions[nextQuestionIndex];

        if (!nextQuestion) return;
        selectedQuestion = nextQuestion;
    };
</script>

<svelte:window on:keyup={handleQuestionSelect} />

{#if tbquestions.length}
    <div transition:slide class="tiebreaker-question-container flex-column">
        <div class="question-nav">
            <button class="nav-left" id="left" on:click={handleQuestionSelect}>
                <DoubleArrow />
            </button>

            <p>{selectedQuestion.question_text}</p>

            {#if selectedQuestion.question_notes}<p><strong>Notes:</strong> {selectedQuestion.question_notes}</p>{/if}

            <button class="nav-right" id="right" on:click={handleQuestionSelect}>
                <DoubleArrow />
            </button>
        </div>

        <button class="button button-secondary" on:click={() => (answerShown = !answerShown)}>
            {answerButtonTxt}
        </button>

        {#if answerShown}
            <div transition:slide class="flex-column">
                <p>{selectedQuestion.display_answer}</p>
                {#if selectedQuestion.answer_notes}<p><strong>Notes:</strong> {selectedQuestion.answer_notes}</p>{/if}
            </div>
        {/if}
    </div>
{:else}
    <p>There are no Tiebreaker questions for this event</p>
{/if}

<style lang="scss">
    .tiebreaker-question-container {
        width: 100%;
        max-width: var(--max-element-width);
    }
    .question-nav {
        width: 100%;
        display: flex;
        justify-content: space-between;
        .nav-left {
            margin: 0 -1rem 0 -2rem;
            rotate: 90deg;
            align-self: center;
        }
        .nav-right {
            margin: 0 -2rem 0 -1rem;
            rotate: -90deg;
            align-self: center;
        }
    }
</style>
