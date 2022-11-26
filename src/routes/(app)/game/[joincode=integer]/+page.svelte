<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import Round from './Round.svelte';
    import Question from './Question.svelte';
    import Note from './Note.svelte';
    import type { EventPageData, ActiveEventData } from '$lib/types';

    // TODO: acitve round/question don't seem to survive HMR, not sure it that existed before

    $: eventPageData = getStore<EventPageData>('eventPageData');
    $: activeEventData = getStore<ActiveEventData>('activeEventData');

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

<h3>{$eventPageData?.activeRound?.title}</h3>

<div class="round-selector">
    {#each $eventPageData.roundNumbers as roundNum}
        <button
            class:active={$eventPageData.activeRoundNumber === roundNum}
            class:current={$eventPageData.currentRoundNumber === roundNum}
            id={String(roundNum)}
            on:click={handleRoundSelect}
        >
            {roundNum}
        </button>
    {/each}
</div>

<Round>
    <Question />
    <Note />
</Round>

<style lang="scss">
    h3 {
        margin: 0.5em 0.25em;
    }
</style>
