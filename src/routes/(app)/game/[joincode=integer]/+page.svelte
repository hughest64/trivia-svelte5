<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import Round from './Round.svelte';
    import Question from './Question.svelte';
    import Note from './Note.svelte';
    import type { CurrentEventData, GameQuestion, ActiveEventData, GameRound, Response } from '$lib/types';

    // TODO: acitve round/question don't seem to survice HMR, not sure it that existed before

    $: currentEventData = getStore<CurrentEventData>('currentEventData');
    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: activeRound = <GameRound>(
        $page.data.rounds?.find((round: GameRound) => round.round_number === $activeEventData.activeRoundNumber)
    );
    $: activeQuestion = <GameQuestion>(
        $page.data.questions?.find((question: GameQuestion) => question.key === $activeEventData.activeQuestionKey)
    );
    // TODO: should this move to the question?
    $: responseStore = getStore<Response[]>('responseData');
    $: activeResponse = $responseStore.find((response) => response.key === activeQuestion?.key);

    $: joincode = $page.params?.joincode;

    const roundNumbers = $page.data.rounds?.map((round: GameRound) => round.round_number) || [];
    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;

        $activeEventData = {
            activeQuestionNumber: 1,
            activeRoundNumber: Number(target.id),
            activeQuestionKey: `${target.id}.1`
        };

        // post to the game endpoint to set active round and question in a cookie
        await fetch('/update', {
            method: 'POST',
            body: JSON.stringify({ activeEventData: $activeEventData, joincode })
        });
    };
</script>

<h3>{activeRound.title}</h3>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        <button
            class:active={$activeEventData.activeRoundNumber === roundNum}
            class:current={$currentEventData.round_number === roundNum}
            id={String(roundNum)}
            on:click={handleRoundSelect}
        >
            {roundNum}
        </button>
    {/each}
</div>

<Round>
    <!-- TODO: could probably get both of these right in the Question -->
    <Question {activeQuestion} {activeResponse} />
    <Note activeQuestionKey={activeQuestion.key} />
</Round>

<style lang="scss">
    h3 {
        margin: 0.5em 0.25em;
    }
</style>
