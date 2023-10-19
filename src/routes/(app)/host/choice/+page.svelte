<script lang="ts">
    import { getStore } from '$lib/utils';

    $: userData = getStore('userData');
</script>

<svelte:head><title>Trivia Mafia | Host or Play</title></svelte:head>

<main class="short">
    <h1>Greetings {$userData?.username || ''}</h1>

    <h3>Do you want to:</h3>

    <!-- NOTE: rel="external" here ensures that the layout load will run and we get our data from the api -->
    <a class="button button-primary" id="host" href="/host/event-setup" rel="external">Host A Game</a>
    <a class="button button-secondary" id="play" href="/team" rel="external">Play Trivia</a>

    <small
        >To view the recent changes in the application, click <a class="changelog-link" href="/changelog">Here.</a
        ></small
    >
</main>

<style>
    small {
        padding: 0 0.5em;
        font-size: 0.75rem;
    }
    a:not(.changelog-link) {
        text-decoration: none;
    }
</style>
