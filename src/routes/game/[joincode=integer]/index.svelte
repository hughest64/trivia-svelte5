<script lang="ts">
    import { activeRound, activeRoundNumber, activeQuestionNumber } from '$stores/event'
    import RoundHeader from '$lib/game/RoundHeader.svelte';
    import Round from "$lib/game/Round.svelte"

    export let initialRoundNumber: number;
    $: initialRoundNumber && activeRoundNumber.set(Number(initialRoundNumber))

    export let initialQuestionNumber: number;
    $: initialQuestionNumber && activeQuestionNumber.set(Number(initialQuestionNumber))

</script>

{#if !!$activeRound}
    <RoundHeader />
    <Round />
{:else}
    <h3>Something Went Wrong!</h3>
    <p>Please refresh the page to try and resovle the issue</p>
{/if}
