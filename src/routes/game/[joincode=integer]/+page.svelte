<script lang="ts">
    import { activeRound, activeRoundNumber, activeQuestionNumber } from '$stores/event';
    import RoundHeader from '$lib/game/RoundHeader.svelte';
    import Round from '$lib/game/Round.svelte';
    
    // TODO: grab $page.data, it should contain the active q/r, if not fallback on current q/r from store
    import { page } from '$app/stores';

    $: initialRoundNumber = $page.data?.initialRoundNumber;
    $: initialRoundNumber && activeRoundNumber.set(Number(initialRoundNumber));

    $: initialQuestionNumber = $page.data?.initialQuestionNumber;
    $: initialQuestionNumber && activeQuestionNumber.set(Number(initialQuestionNumber));
</script>

{#if !!$activeRound}
    <RoundHeader />
    <Round />
{:else}
    <h3>Something Went Wrong!</h3>
    <p>Please refresh the page to try and resolve the issue</p>
{/if}
