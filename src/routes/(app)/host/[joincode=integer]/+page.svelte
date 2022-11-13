<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import Round from './Round.svelte';
    import type { ActiveEventData, CurrentEventData, GameRound } from '$lib/types';

    const eventData = $page.data.event_data;
    const rounds = $page.data.rounds || [];

    $: activeData = getStore<ActiveEventData>('activeEventData');
    $: currentEventData = getStore<CurrentEventData>('currentEventData');
    $: activeRound = <GameRound>rounds.find((round: GameRound) => round.round_number === $activeData.activeRoundNumber);
    $: roundNumbers = rounds.map((round: GameRound) => round.round_number);

    $: joincode = $page.params?.joincode;

    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;

        $activeData = {
            activeQuestionNumber: 1,
            activeRoundNumber: Number(target.id),
            activeQuestionKey: `1.${target.id}`
        };

        // post to the game endpoint to set active round and question in a cookie
        await fetch('/update', {
            method: 'POST',
            body: JSON.stringify({ activeData: $activeData, joincode })
        });
    };

    // TODO: fix when actually locking rounds
    let checked = false;
    const handleLockRound = async () => {
        checked = !checked;
        // const response = await fetch('some url', {
        //     method: 'POST',
        //     // we should have the proper headers in $page.data (I think) if we need them
        //     // headers: {}
        //     body: ''
        // });
    };
</script>

<h1>Host Game</h1>
<p>Event Join Code: <strong>{joincode}</strong></p>
<p>Details: <strong>{eventData?.location}, {eventData?.game_title}</strong></p>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        <button
            id={String(roundNum)}
            on:click={handleRoundSelect}
            class:active={$activeData.activeRoundNumber === roundNum}
            class:current={$currentEventData.round_number === roundNum}
        >
            {roundNum}
        </button>
    {/each}
</div>

<div class="lock-container">
    <label for="round-lock" class="lock">
        <input
            type="checkbox"
            name="round-lock"
            id="round-lock"
            bind:checked
            on:click|preventDefault={handleLockRound}
        />
        <span class:checked />
    </label>
</div>

<!-- TODO: should this be an anchor or do we have actions to execute here?
this is also conditionally displayed based on lock status and the text needs updating -->
<button class="button button-red" on:click|preventDefault>Score/Edit This Round</button>

<Round {activeRound} />

<style lang="scss">
    h1 {
        margin: 0.5em 0.25em;
    }

    p {
        margin: 1em 0.25em;
    }

    .lock-container {
        .lock {
            position: relative;
            display: inline-block;
            width: 6em;
            height: 6em;
            input {
                opacity: 0;
                width: 0;
                height: 0;
            }
            span {
                position: absolute;
                cursor: pointer;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20viewBox%3D%220%200%2033.073%2033.073%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20transform%3D%22translate(8.021%20-4.473)%22%3E%3Crect%20width%3D%2221.167%22%20height%3D%2216.057%22%20x%3D%22-2.068%22%20y%3D%2218.89%22%20ry%3D%222.45%22%20fill%3D%22%23413f43%22%20fill-rule%3D%22evenodd%22%2F%3E%3Cpath%20d%3D%22M-2.068%2032.497v.001c0%20.369.08.717.225%201.03h20.716c.144-.313.225-.661.225-1.03v-.001z%22%20fill%3D%22%236fcf97%22%20fill-rule%3D%22evenodd%22%2F%3E%3Cg%20transform%3D%22matrix(.29195%200%200%20.29195%20-71.867%20-7.993)%22%20fill%3D%22%236fcf97%22%3E%3Ccircle%20cx%3D%22275.324%22%20cy%3D%22117.241%22%20r%3D%226.25%22%2F%3E%3Cpath%20d%3D%22M271.337%20115.843h7.974v12.321h-7.974z%22%2F%3E%3C%2Fg%3E%3Cpath%20d%3D%22M17.715%207.353a5.953%205.953%200%2000-5.953%205.953v5.945h2.706v-6.088h.008a3.247%203.247%200%20013.24-3.105%203.247%203.247%200%20013.243%203.105h.004V15.053h2.705v-1.747a5.953%205.953%200%2000-5.953-5.953z%22%20fill%3D%22%23413f43%22%20fill-rule%3D%22evenodd%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E');
            }
            .checked {
                background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20viewBox%3D%220%200%2033.073%2033.073%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20transform%3D%22matrix(1.00296%200%200%201.00296%20-.049%20-.043)%22%3E%3Crect%20width%3D%2221.104%22%20height%3D%2216.01%22%20x%3D%225.984%22%20y%3D%2214.417%22%20ry%3D%222.443%22%20fill%3D%22%23413f43%22%20fill-rule%3D%22evenodd%22%2F%3E%3Cpath%20d%3D%22M5.984%2027.984v.001c0%20.368.081.715.225%201.027h20.655c.144-.312.225-.66.225-1.027v-.001z%22%20fill%3D%22%23dc0926%22%20fill-rule%3D%22evenodd%22%2F%3E%3Cg%20transform%3D%22matrix(.2911%200%200%20.2911%20-63.608%20-12.386)%22%20fill%3D%22%23dc0926%22%3E%3Ccircle%20cx%3D%22275.324%22%20cy%3D%22117.241%22%20r%3D%226.25%22%2F%3E%3Cpath%20d%3D%22M271.337%20115.843h7.974v12.321h-7.974z%22%2F%3E%3C%2Fg%3E%3C%2Fg%3E%3Cpath%20d%3D%22M16.536%207.027a5.953%205.953%200%2000-5.953%205.953v5.945h2.707v-6.088h.008a3.247%203.247%200%20013.238-3.104%203.247%203.247%200%20013.244%203.104h.004V14.727h2.706V12.98a5.953%205.953%200%2000-5.954-5.953z%22%20fill%3D%22%23413f43%22%20fill-rule%3D%22evenodd%22%2F%3E%3C%2Fsvg%3E');
            }
        }
    }
</style>
