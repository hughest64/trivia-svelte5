<!--
    TODO: 
    - add an endpoint file for handling active round/question like game index
    - create a host version of round numbers
    - create a host version of round
 -->
 <script lang="ts">
    import { page } from '$app/stores'
    import { eventRounds, activeRoundNumber, activeQuestionNumber } from '$stores/event'
    import RoundHeader from '$lib/host/RoundHeader.svelte';
    import Round from '$lib/host/Round.svelte'

    const joincode = $page.params.joincode
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