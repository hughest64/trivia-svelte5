<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import Round from './Round.svelte';
    import Question from './Question.svelte';
    import Note from './Note.svelte';
    import type { GameQuestion, ActiveEventData, EventData, GameRound, Response } from '$lib/types';

    $: activeData = getStore<ActiveEventData>('activeEventData');
    $: eventData = getStore<EventData>('eventData');
    $: rounds = getStore<GameRound[]>('rounds');
    $: questions = getStore<GameQuestion[]>('questions');
    $: responseStore = getStore<Response[]>('responseData');
    $: activeRound = $rounds?.find((round) => round.round_number === $activeData.activeRoundNumber) || $rounds[0];
    $: activeQuestion = $questions.find((question) => question.key === $activeData.activeQuestionKey) || $questions[0];
    $: activeResponse = $responseStore.find((response) => response.key === activeQuestion.key);
    $: roundNumbers = $rounds.map((round) => round.round_number);

    $: joincode = $page.params?.joincode;

    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;

        $activeData = {
            activeQuestionNumber: 1,
            activeRoundNumber: Number(target.id),
            activeQuestionKey: `${target.id}.1`
        };

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

<Round questions={$questions} {activeData} activeQuestionKey={activeQuestion.key}>
    <Question {activeQuestion} {activeResponse} />
    <Note activeQuestionKey={activeQuestion.key} />
</Round>

<style lang="scss">
    h3 {
        margin: 0.5em 0.25em;
    }
</style>
