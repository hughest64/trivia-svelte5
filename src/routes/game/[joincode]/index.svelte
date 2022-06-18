<script lang="ts">
    // TODO: all of this should probably be in __layout
    import { page } from '$app/stores'
    import { eventData, type EventRound } from '$stores/event'
    import RoundHeader from '$lib/RoundHeader.svelte';
    import Round from "$lib/Round.svelte"

    const joincode = $page.params.joincode

    // TODO: probably better to split this data out to separate stores, maybe in __layout?
    $: currentQuestion = $eventData.current_question
    $: currentRound = $eventData.current_round
    $: roundNumbers = $eventData?.rounds.map((round) => round.round_number)
    // TODO: we'll pull the current round data from a currentRoundIndex store value
    $: roundData = $eventData.rounds.find( round => round.round_number === currentRound) as EventRound

</script>

<h1>Welcome to Game {joincode}</h1>

<div class="container">
    {#if $eventData}
        <RoundHeader bind:roundNumbers />
        <Round bind:roundData bind:currentQuestion />
    {:else}
        <h3>No Data!</h3>
    {/if}
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: .75em;
        max-width: 30rem;
        margin: 5rem auto 0;
    }
</style>