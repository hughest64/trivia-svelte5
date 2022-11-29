<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import Round from './Round.svelte';
    import Question from './Question.svelte';
    import Note from './Note.svelte';
    import type { CurrentEventData, ActiveEventData, GameRound } from '$lib/types';

    const roundNumbers = $page.data?.rounds?.map((rd) => rd.round_number) || []; 
    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: currentEventData = getStore<CurrentEventData>('currentEventData');
    $: activeRound = $page.data?.rounds?.find((rd) => rd.round_number === $activeEventData.activeRoundNumber) as GameRound;

    $: joincode = $page.params?.joincode;

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

<h3>{activeRound?.title}</h3>

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

<Round {activeRound}>
    <Question />
    <Note />
</Round>

<style lang="scss">
    h3 {
        margin: 0.5em 0.25em;
    }
</style>
