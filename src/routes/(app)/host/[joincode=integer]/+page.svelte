<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import { deserialize } from '$app/forms';
    import Round from './Round.svelte';
    import RoundSelector from './RoundSelector.svelte';
    import type { GameRound } from '$lib/types';

    const eventData = $page.data.event_data;
    const popupData = getStore('popupData');
    const activeEventData = getStore('activeEventData');
    const roundStates = getStore('roundStates') || [];

    $: activeRound = $page.data.rounds?.find(
        (rd) => rd.round_number === $activeEventData.activeRoundNumber
    ) as GameRound;
    $: activeRoundState = $roundStates.find((rs) => rs.round_number === $activeEventData.activeRoundNumber);
    $: locked = activeRoundState?.locked;

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
                error = result.data?.error || 'An Error Occured';
                locked = !locked;
            }
        }
    };
</script>

<div class="title-container flex-column">
    <h1>Host Game</h1>
    <h4>Event Join Code: <strong>{joincode}</strong></h4>
    <h4>Details: <strong>{eventData?.location}, {eventData?.game_title}</strong></h4>
</div>
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

<!-- <button class="button button-primary" on:click|preventDefault>Score/Edit This Round</button> -->

<Round {activeRound} />
