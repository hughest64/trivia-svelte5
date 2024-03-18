<script lang="ts">
    import { page } from '$app/stores';
    import { deserialize } from '$app/forms';
    import Round from './Round.svelte';
    import RoundSelector from './RoundSelector.svelte';

    import { getState } from '$lib/state/utils.svelte';
    const evh = getState('eventHandler');
    // $inspect(evh.activeRoundState);

    let locked = $state(evh.activeRoundState?.locked);
    let scoreButtonText = $derived(evh.activeRoundState?.scored ? 'Edit This Rounds Scores' : 'Score This Round');

    const joincode = $page.params?.joincode;

    let error = $state<string>();
    const handleLockRound = async () => {
        error = '';
        // if (locked) {
        //     TODO: s5 - we need an updated popupHandler
        //     $popupData = {
        //         popup_type: 'round_unlock',
        //         is_displayed: true,
        //         data: { roundNumber: activeRound?.round_number }
        //     };
        // } else {
        locked = !locked;

        const data = new FormData();
        data.set('round_number', String(evh.activeRound?.round_number));
        data.set('locked', locked ? 'true' : 'false');

        const response = await fetch('?/lock', { method: 'post', body: data });
        const result = deserialize(await response.text());
        if (result.type === 'failure') {
            error = (result.data?.error as string) || 'An Error Occured';
            locked = !locked;
        }
        // }
    };
    // TDOO: perhaps set to this round if button text says "edit"
    // otherwise use the min if unscored (revealed?) rounds
    const setActiveQuestion = () => {
        evh.activeEventData = evh.setActiveEventData(1, evh.activeRound?.round_number, undefined, true);
    };
</script>

<div class="host-container flex-column">
    <h1>Host Game</h1>
    <h4 id="event-joincode">Event Join Code: <strong>{joincode}</strong></h4>
    <h4 id="event-details">Details: <strong>{evh.event_data?.location}, {evh.event_data?.game_title}</strong></h4>

    <RoundSelector />

    <div class="lock-container">
        <label id={`rd-${evh.activeRound?.round_number}`} for="round-lock" class="lock">
            <input
                type="checkbox"
                name="round-lock"
                id="round-lock"
                bind:checked={locked}
                on:click|preventDefault={handleLockRound}
            />
            <span class:checked={locked} />
        </label>
    </div>
    {#if error}<p>{error}</p>{/if}

    {#if locked}
        <a
            class="button button-primary"
            data-sveltekit-reload
            href={`/host/${joincode}/score`}
            on:click={setActiveQuestion}>{scoreButtonText}</a
        >
    {/if}
</div>

<Round activeRound={evh.activeRound} />

<div class="lock-container">
    {#if error}<p>{error}</p>{/if}
    <label id={`rd-${evh.activeRound?.round_number}`} for="round-lock" class="lock">
        <input
            type="checkbox"
            name="round-lock"
            id="round-lock"
            bind:checked={locked}
            on:click|preventDefault={handleLockRound}
        />
        <span class:checked={locked} />
    </label>
</div>
