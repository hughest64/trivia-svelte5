 <script lang="ts">
    import { page } from '$app/stores';
    import { activeRoundNumber } from '$stores/event';
    import RoundHeader from '$lib/host/RoundHeader.svelte';
    import Round from '$lib/host/Round.svelte';

    export let initialRoundNumber: number;
    $: initialRoundNumber && activeRoundNumber.set(Number(initialRoundNumber));

    const joincode = $page.params.joincode;
 </script>

<h1>Good Luck Hosting Game {joincode}!</h1>

<div class="container">
    <RoundHeader />
    <Round />
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