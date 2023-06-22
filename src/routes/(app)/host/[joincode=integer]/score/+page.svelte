<script lang="ts">
    import { page } from '$app/stores';
    import { getStore, setEventCookie } from '$lib/utils';
    import RoundSelector from '../RoundSelector.svelte';
    import ResponseGroup from './ResponseGroup.svelte';

    const rounds = getStore('rounds');
    const allQuestions = getStore('questions');
    const roundNumbers = $rounds.map((rd) => rd.round_number) || [];
    const joincode = $page.params.joincode;
    const questionKeys = $allQuestions.map((q) => Number(q.key));

    const activeEventData = getStore('activeEventData');
    const responses = getStore('hostResponseData');

    $: roundNumber = $activeEventData.activeRoundNumber;
    $: roundQuestions = $allQuestions.filter((q) => q.round_number === roundNumber);
    $: roundQuestionNumbers = roundQuestions?.map((q) => q.question_number) || [];

    $: scoringQuestionNumber = $activeEventData.activeQuestionNumber || 1;
    $: scoringQuestion = roundQuestions.find((q) => q.question_number === scoringQuestionNumber);
    $: scoringResponses = ($responses && $responses.filter((r) => r.key === $activeEventData.activeQuestionKey)) || [];

    $: isFirstQuestion = Number($activeEventData.activeQuestionKey) === Math.min(...questionKeys);
    $: isLastQuestion = Number($activeEventData.activeQuestionKey) === Math.max(...questionKeys);

    const advance = async () => {
        const next = scoringQuestionNumber + 1;
        const maxQuestion = Math.max(...roundQuestionNumbers);
        const maxRound = Math.max(...roundNumbers);

        if (next <= maxQuestion) {
            activeEventData.update((data) => ({
                ...data,
                activeQuestionKey: `${roundNumber}.${next}`,
                activeQuestionNumber: next
            }));
        } else if (next > maxQuestion) {
            const nextRound = roundNumber + 1;
            if (roundNumber < maxRound) {
                $activeEventData = {
                    activeRoundNumber: nextRound,
                    activeQuestionNumber: 1,
                    activeQuestionKey: `${nextRound}.1`
                };
            }
        }
        setEventCookie($activeEventData, joincode);
    };

    const goBack = async () => {
        const previousQ = scoringQuestionNumber - 1;
        const minQuestion = Math.min(...roundQuestionNumbers);

        if (previousQ >= minQuestion) {
            activeEventData.update((data) => ({
                ...data,
                activeQuestionKey: `${roundNumber}.${previousQ}`,
                activeQuestionNumber: previousQ
            }));
        } else if (previousQ < minQuestion) {
            const minRound = Math.min(...roundNumbers);
            const previousround = roundNumber - 1;
            if (roundNumber > minRound) {
                const previousRoundMaxQ = Math.max(
                    ...$allQuestions.filter((q) => q.round_number === previousround).map((q) => q.question_number)
                );
                $activeEventData = {
                    activeRoundNumber: previousround,
                    activeQuestionNumber: previousRoundMaxQ,
                    activeQuestionKey: `${previousround}.${previousRoundMaxQ}`
                };
            }
        }
        setEventCookie($activeEventData, joincode);
    };

    const handleKeyPress = (event: KeyboardEvent) => {
        if (event.code === 'ArrowRight') {
            advance();
        } else if (event.code === 'ArrowLeft') {
            goBack();
        }
    };
</script>

<svelte:window on:keyup={handleKeyPress} />

<div class="host-container flex-column">
    <h1>Scoring</h1>
    <RoundSelector />
</div>

<!-- TODO: better handling of this, it gets weird if a question doesn't have any responses, but the next question does -->
<!-- {#if scoringResponses.length > 0} -->
<div class="host-question-panel">
    <h2>Round {scoringQuestion?.round_number} Question {scoringQuestion?.question_number}</h2>
    <p>{scoringQuestion?.question_text}</p>
</div>

<h4 class="answer">Answer: {scoringQuestion?.display_answer}</h4>

<div class="button-container">
    <button class="button button-secondary" disabled={isFirstQuestion} on:click={goBack}>Previous</button>
    {#if !isLastQuestion}
        <button class="button button-secondary" on:click={advance}>Next</button>
    {:else}
        <!-- TODO: query param that will set active event data to the min of unscored rounds -->
        <!-- (see notes in Footer.svelte, I think an after navigate will handle it) -->
        <a href="/host/{joincode}" class="button button-primary">Go Read Answers Aloud</a>
    {/if}
</div>

<ul id="response-groups">
    {#each scoringResponses as response}
        <ResponseGroup {response} />
    {/each}
</ul>

<div class="button-container">
    <button class="button button-secondary" disabled={isFirstQuestion} on:click={goBack}>Previous</button>
    {#if !isLastQuestion}
        <button class="button button-secondary" on:click={advance}>Next</button>
    {:else}
        <a href="/host/{joincode}" class="button button-primary">Go Read Answers Aloud</a>
    {/if}
</div>

<!-- {:else}
    <h2>All Caught Up!</h2>
{/if} -->
<style lang="scss">
    .button-container {
        width: 40em;
        max-width: calc(100% - 2em);
        display: flex;
        gap: 1rem;
    }
</style>
