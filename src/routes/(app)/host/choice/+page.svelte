<script lang="ts">
    import { page } from '$app/stores';

    $: userData = $page.data?.user_data;
</script>

<svelte:head><title>Trivia Mafia | Host or Play</title></svelte:head>

<h1>Greetings {userData?.username || ''}</h1>

<h3>Do you want to:</h3>

<!-- NOTE: rel="external" here ensures that the layout load will run and we get our data from the api -->
<a class="button button-red" id="host" href="/host/event-setup" rel="external">Host A Game</a>
<a class="button button-black" id="play" href="/team" rel="external">Play Trivia</a>

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