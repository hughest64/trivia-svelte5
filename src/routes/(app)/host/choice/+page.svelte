<script lang="ts">
    import { page } from '$app/stores';

    $: userData = $page.data?.user_data;
</script>

<svelte:head><title>Trivia Mafia | Host or Play</title></svelte:head>

<h1>Greetings {userData?.username || ''}</h1>

<h3>Do you want to:</h3>

<a class="button button-red" id="host" href="/host/event-setup">Host A Game</a>
<a class="button button-black" id="play" href="/team">Play Trivia</a>

<small>To view the recent changes in the application, click Here.</small>

<style>
    h1,
    h3 {
        margin: 0.75em 0;
    }
    small {
        padding: 0 0.5em;
        font-size: 12px;
    }
    a {
        text-decoration: none;
    }
</style>