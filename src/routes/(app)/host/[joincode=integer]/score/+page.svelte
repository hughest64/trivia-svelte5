<script lang="ts">
    import { page } from '$app/stores';
    import { getStore, setEventCookie } from '$lib/utils';
    import RoundSelector from '../RoundSelector.svelte';
    import ResponseGroup from './ResponseGroup.svelte';

    const rounds = getStore('rounds');
    const roundStates = getStore('roundStates');
    const allQuestions = getStore('questions');
    const roundNumbers = $rounds.map((rd) => rd.round_number) || [];
    const joincode = $page.params.joincode;
    const questionKeys = $allQuestions.map((q) => Number(q.key));

    const activeEventData = getStore('activeEventData');
    const responses = getStore('hostResponseData');

    $: roundNumber = $activeEventData.activeRoundNumber;
    $: activeRoundIsLocked = $roundStates.find((rs) => rs.round_number === roundNumber)?.locked;
    $: roundQuestions = $allQuestions.filter((q) => q.round_number === roundNumber);
    $: roundQuestionNumbers = roundQuestions?.map((q) => q.question_number) || [];

    $: scoringQuestionNumber = $activeEventData.activeQuestionNumber || 1;
    $: scoringQuestion = roundQuestions.find((q) => q.question_number === scoringQuestionNumber);
    $: scoringResponses = ($responses && $responses.filter((r) => r.key === $activeEventData.activeQuestionKey)) || [];

    $: isFirstQuestion = Number($activeEventData.activeQuestionKey) === Math.min(...questionKeys);
    $: isLastQuestion = Number($activeEventData.activeQuestionKey) === Math.max(...questionKeys);

    $: minUnscoredRound = Math.min(...$roundStates.filter((rs) => !rs.scored).map((rs) => rs.round_number));
    $: readAnswersLink = `/host/${joincode}?active-key=${minUnscoredRound}.1`;

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

{#if activeRoundIsLocked}
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
            <a href={readAnswersLink} class="button button-primary read-info" on:click>Go Read Answers Aloud</a>
        {/if}
    </div>

    <ul id="response-groups">
        {#if scoringResponses.length > 0}
            {#each scoringResponses as response}
                <ResponseGroup {response} />
            {/each}
        {:else}
            <h4 class="no-resp">There are no responses to this question</h4>
        {/if}
    </ul>

    <div class="button-container">
        <button class="button button-secondary" disabled={isFirstQuestion} on:click={goBack}>Previous</button>
        {#if !isLastQuestion}
            <button class="button button-secondary" on:click={advance}>Next</button>
        {:else}
            <a href={readAnswersLink} class="button button-primary">Go Read Answers Aloud</a>
        {/if}
    </div>
{:else}
    <h2 class="read-info">Round {roundNumber} is not locked</h2>
    <a href={readAnswersLink} class="button button-primary read-info">Go Read Answers Aloud</a>
{/if}

<style lang="scss">
    .button-container {
        width: 40em;
        max-width: calc(100% - 2em);
        display: flex;
        gap: 1rem;
    }
    .read-info {
        width: var(--max-element-width);
        max-width: calc(100% - 2rem);
        text-align: center;
    }
    .no-resp {
        padding: 0 1rem;
    }
</style>
