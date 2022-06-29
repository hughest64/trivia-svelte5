<script lang="ts">
    import { page } from '$app/stores'
    import { eventRounds, activeRoundNumber, activeQuestionNumber } from '$stores/event'
    import RoundHeader from '$lib/game/RoundHeader.svelte';
    import Round from "$lib/game/Round.svelte"

    export let initialRoundNumber: number;
    $: initialRoundNumber && activeRoundNumber.set(Number(initialRoundNumber))

    export let initialQuestionNumber: number;
    $: initialQuestionNumber && activeQuestionNumber.set(Number(initialQuestionNumber))

    const joincode = $page.params.joincode

</script>

<h1>Welcome to Game {joincode}</h1>

<div class="container">
    {#if $eventRounds}
        <RoundHeader />
        <Round />
    {:else}
        <h3>Something Went Wrong!</h3>
        <p>Please refresh the page to try and resovle the issue</p>
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