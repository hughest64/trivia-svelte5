<script lang="ts">
    import { page } from '$app/stores';
    import { getStore, setEventCookie } from '$lib/utils';
    import { deserialize } from '$app/forms';
    import Round from './Round.svelte';
    import RoundSelector from './RoundSelector.svelte';
    import type { GameRound } from '$lib/types';

    import { getState } from '$lib/state/utils.svelte';
    const eventHandler = getState('eventHandler');
    $: console.log(eventHandler);

    const eventData = getStore('eventData');
    const rounds = getStore('rounds');
    const popupData = getStore('popupData');
    const activeEventData = getStore('activeEventData');
    const roundStates = getStore('roundStates') || [];

    $: activeRound = $rounds?.find((rd) => rd.round_number === $activeEventData.activeRoundNumber) as GameRound;
    $: activeRoundState = $roundStates?.find((rs) => rs.round_number === $activeEventData.activeRoundNumber);
    $: locked = activeRoundState?.locked;
    $: scoreButtonText = activeRoundState?.scored ? 'Edit This Rounds Scores' : 'Score This Round';

    $: joincode = $page.params?.joincode;

    let error: string;
    const handleLockRound = async () => {
        error = '';
        if (locked) {
            $popupData = {
                popup_type: 'round_unlock',
                is_displayed: true,
                data: { roundNumber: activeRound?.round_number }
            };
        } else {
            locked = !locked;

            const data = new FormData();
            data.set('round_number', String(activeRound?.round_number));
            data.set('locked', locked ? 'true' : 'false');

            const response = await fetch('?/lock', { method: 'post', body: data });
            const result = deserialize(await response.text());
            if (result.type === 'failure') {
                error = (result.data?.error as string) || 'An Error Occured';
                locked = !locked;
            }
        }
    };
    // TDOO: perhaps set to this round if button text says "edit"
    // otherwise use the min if unscored (revealed?) rounds
    const setActiveQuestion = () => {
        $activeEventData = {
            activeRoundNumber: Number(activeRound.round_number),
            activeQuestionNumber: 1,
            activeQuestionKey: `${activeRound.round_number}.1`
        };
        setEventCookie($activeEventData, $page.params.joincode);
    };
</script>

<div class="host-container flex-column">
    <h1>Host Game</h1>
    <h4 id="event-joincode">Event Join Code: <strong>{joincode}</strong></h4>
    <h4 id="event-details">Details: <strong>{$eventData?.location}, {$eventData?.game_title}</strong></h4>

    <RoundSelector />

    <div class="lock-container">
        <label id={`rd-${activeRound?.round_number}`} for="round-lock" class="lock">
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

<Round {activeRound} />

<div class="lock-container">
    {#if error}<p>{error}</p>{/if}
    <label id={`rd-${activeRound?.round_number}`} for="round-lock" class="lock">
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
