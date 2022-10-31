<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import Round from './Round.svelte';
    import Question from './Question.svelte';
    import Note from './Note.svelte';
    import type { ActiveEventData, EventData, Response } from '$lib/types';

    $: activeData = getStore<ActiveEventData>('activeEventData');
    $: eventData = getStore<EventData>('eventData');
    $: responseStore = getStore<Response[]>('responseData');

    $: activeRound =
        $eventData?.rounds.find((round) => round.round_number === $activeData.activeRoundNumber) ||
        $eventData.rounds[0];

    $: activeQuestion =
        activeRound.questions.find((question) => question.question_number === $activeData.activeQuestionNumber) ||
        activeRound?.questions[0];

    $: activeRoundQuestion = `${activeRound.round_number}.${activeQuestion.question_number}`;
    $: activeResponse = $responseStore.find((response) => response.key === activeRoundQuestion);
    $: roundNumbers = $eventData?.rounds.map((round) => round.round_number);

    $: joincode = $page.params?.joincode;

    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;

        $activeData = { activeQuestionNumber: 1, activeRoundNumber: Number(target.id) };

        // post to the game endpoint to set active round and question in a cookie
        await fetch('/update', {
            method: 'POST',
            body: JSON.stringify({ activeData: $activeData, joincode })
        });
    };
</script>

<h3>{activeRound.title}</h3>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        <button
            class:active={$activeData.activeRoundNumber === roundNum}
            class:current={$eventData.current_round_number === roundNum}
            id={String(roundNum)}
            on:click={handleRoundSelect}
        >
            {roundNum}
        </button>
    {/each}
</div>

<Round {activeRound} {activeData} activeQuestionKey={activeQuestion.key}>
    <Question {activeQuestion} {activeResponse} />
    <Note activeRoundQuestion={activeQuestion.key} />
</Round>

<style lang="scss">
    h3 {
        margin: 0.5em 0.25em;
    }
</style>
