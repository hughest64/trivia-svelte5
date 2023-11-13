<script lang="ts">
    import { page } from '$app/stores';
    import { slide } from 'svelte/transition';
    import { swipeQuestion } from '$lib/swipe';
    import DoubleArrow from '$lib/footer/icons/DoubleArrow.svelte';

    const tbquestions = $page.data.tiebreaker_questions || [];
    export let selectedQuestion = tbquestions[0];
    $: selectedQuestionIndex = tbquestions.findIndex((q) => q.id === selectedQuestion?.id);

    let answerShown = false;
    $: answerButtonTxt = answerShown ? 'Hide Answer' : 'Show Answer';

    const handleQuestionSelect = async (event: MouseEvent | CustomEvent | KeyboardEvent) => {
        const eventDirection = event.detail?.direction;
        const keyCode = (event as KeyboardEvent).code;

        let nextQuestionIndex = selectedQuestionIndex;
        if (eventDirection === 'left' || keyCode === 'ArrowLeft') {
            nextQuestionIndex -= 1;
        } else if (eventDirection === 'right' || keyCode === 'ArrowRight') {
            nextQuestionIndex += 1;
        }
        const nextQuestion = tbquestions[nextQuestionIndex];

        if (!nextQuestion) return;
        selectedQuestion = nextQuestion;
    };
</script>

<svelte:window on:keyup={handleQuestionSelect} />

<!-- TODO: probably change to swipe -->
{#if tbquestions.length}
    <div
        transition:slide
        class="tiebreaker-question-container flex-column"
        use:swipeQuestion
        on:swipe={handleQuestionSelect}
    >
        <div class="question-nav">
            <button class="nav-left">
                <DoubleArrow />
            </button>
            <p>{selectedQuestion.question_text}</p>
            {#if selectedQuestion.question_notes}<p><strong>Notes:</strong> {selectedQuestion.question_notes}</p>{/if}
            <button class="nav-right">
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
        // outline: 1px dashed red;
    }
    .question-nav {
        width: 100%;
        display: flex;
        justify-content: space-between;
        .nav-left {
            // padding: 0;
            margin: 0 -1rem 0 -2rem;
            rotate: 90deg;
            align-self: center;
        }
        .nav-right {
            // padding: 0;
            margin: 0 -2rem 0 -1rem;
            // margin-right: -2rem;
            rotate: -90deg;
            align-self: center;
        }
    }
</style>
