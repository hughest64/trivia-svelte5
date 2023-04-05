<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import RoundSelector from '../RoundSelector.svelte';
    import ResponseGroup from './ResponseGroup.svelte';

    const rounds = getStore('rounds');
    const allQuestions = getStore('questions');
    const roundNumbers = $rounds.map((rd) => rd.round_number) || [];
    // const allQuestions = $questions || [];
    const joincode = $page.params.joincode;

    const activeEventData = getStore('activeEventData');
    const responses = getStore('hostResponseData');

    $: roundNumber = $activeEventData.activeRoundNumber;
    $: roundQuestions = $allQuestions.filter((q) => q.round_number === roundNumber);
    $: roundQuestionNumbers = roundQuestions?.map((q) => q.question_number) || [];

    $: scoringQuestionNumber = $activeEventData.activeQuestionNumber || 1;
    $: scoringQuestion = roundQuestions.find((q) => q.question_number === scoringQuestionNumber);
    $: scoringResponses = ($responses && $responses.filter((r) => r.key === $activeEventData.activeQuestionKey)) || [];

    const advance = async () => {
        const next = scoringQuestionNumber + 1;
        const maxQuestion = Math.max(...roundQuestionNumbers);
        if (next <= maxQuestion) {
            activeEventData.update((data) => ({
                ...data,
                activeQuestionKey: `${roundNumber}.${next}`,
                activeQuestionNumber: next
            }));
            await fetch('/update', {
                method: 'post',
                body: JSON.stringify({ activeEventData: $activeEventData, joincode: joincode })
            });
        } else if (next > maxQuestion) {
            const maxRound = Math.max(...roundNumbers);
            const nextRound = roundNumber + 1;
            if (roundNumber < maxRound) {
                const postData = {
                    activeRoundNumber: nextRound,
                    activeQuestionNumber: 1,
                    activeQuestionKey: `${nextRound}.1`
                };
                $activeEventData = postData;
                await fetch('/update', {
                    method: 'post',
                    body: JSON.stringify({ activeEventData: postData, joincode: joincode })
                });
            }
        }
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
            await fetch('/update', {
                method: 'post',
                body: JSON.stringify({ activeEventData: $activeEventData, joincode: joincode })
            });
        } else if (previousQ < minQuestion) {
            const minRound = Math.min(...roundNumbers);
            const previousround = roundNumber - 1;
            if (roundNumber > minRound) {
                const previousRoundMaxQ = Math.max(
                    ...$allQuestions.filter((q) => q.round_number === previousround).map((q) => q.question_number)
                );
                const postData = {
                    activeRoundNumber: previousround,
                    activeQuestionNumber: previousRoundMaxQ,
                    activeQuestionKey: `${previousround}.${previousRoundMaxQ}`
                };
                $activeEventData = postData;
                await fetch('/update', {
                    method: 'post',
                    body: JSON.stringify({ activeEventData: postData, joincode: joincode })
                });
            }
        }
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

{#if scoringResponses.length > 0}
    <div class="host-question-panel">
        <h2>Round {scoringQuestion?.round_number} Question {scoringQuestion?.question_number}</h2>
        <p>{scoringQuestion?.question_text}</p>
    </div>

    <h4 class="answer">Answer: {scoringQuestion?.display_answer}</h4>

    <div class="button-container">
        <button class="button button-secondary" on:click={goBack}>Previous</button>
        <button class="button button-secondary" on:click={advance}>Next</button>
    </div>

    <ul id="response-groups">
        {#each scoringResponses as response}
            <ResponseGroup {response} />
        {/each}
    </ul>

    <div class="button-container">
        <button class="button button-secondary" on:click={goBack}>Previous</button>
        <button class="button button-secondary" on:click={advance}>Next</button>
    </div>
{:else}
    <h2>All Caught Up!</h2>
{/if}

<style lang="scss">
    .button-container {
        width: 40em;
        max-width: calc(100% - 2em);
        display: flex;
        gap: 1rem;
    }
</style>
