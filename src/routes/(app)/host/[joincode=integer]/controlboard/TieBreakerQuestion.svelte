<script lang="ts">
    import { page } from '$app/stores';
    import { slide } from 'svelte/transition';
    import { swipeQuestion } from '$lib/swipe';

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
{#key selectedQuestion.id}
    <div
        transition:slide
        class="tiebreaker-question-container flex-column"
        use:swipeQuestion
        on:swipe={handleQuestionSelect}
    >
        <p>{selectedQuestion.question_text}</p>
        {#if selectedQuestion.question_notes}<p><strong>Notes:</strong> {selectedQuestion.question_notes}</p>{/if}
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
{/key}

<style lang="scss">
    .tiebreaker-question-container {
        max-width: calc(100% - 2rem);
    }
</style>
