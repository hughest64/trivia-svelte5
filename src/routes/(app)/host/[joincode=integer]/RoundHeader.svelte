<script lang="ts">
    import type { Writable } from 'svelte/store';
    import type { ActiveEventData, EventData, EventRound } from '$lib/types';

    export let activeData: Writable<ActiveEventData>;
    export let eventData: Writable<EventData>;
    export let activeRound: EventRound;
    export let roundNumbers: number[];

    const handleRoundSelect = async (/* event: MouseEvent */) => {
        /**
        const target = <HTMLButtonElement>event.target;
        activeRoundNumber.set(Number(target.id));
        // always reset the question when changing rounds
        activeQuestionNumber.set(1);
        // post to the game endpoint to set active round and question in a cookie
        await fetch(`/host/${joinCode}`, {
            method: 'POST',
            body: JSON.stringify({
                initialRoundNumber: target.id,
                initialQuestionNumber: 1
            })
        });
        */
    };
</script>

<h3>{activeRound.title}</h3>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        <button
            id={String(roundNum)}
            on:click={handleRoundSelect}
            class:active={$activeData.activeRoundNumber === roundNum}
            class:current={$eventData.current_round_number === roundNum}
        >
            {roundNum}
        </button>
    {/each}
</div>

<style lang="scss">
    h3 {
        margin: 0.5em 0.25em;
    }
    .round-selector {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 0.25em;
        max-width: calc(100% - 2em);
        button {
            width: 3em;
            height: 3em;
            border: 2px solid var(--color-black);
            border-radius: 0.5em;
            font-size: 1em;
            font-weight: bold;
            color: var(--color-black);
            background-color: var(--color-white);
            cursor: pointer;
            &.active {
                color: var(--color-white);
                background-color: var(--color-red);
            }
            &.current {
                border-color: var(--color-current);
            }
        }
    }
</style>
