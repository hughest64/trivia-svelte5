<script lang="ts">
    import { page } from '$app/stores';
    import { afterNavigate, goto } from '$app/navigation';

    $: userData = $page.data?.user_data;
    // TODO:
    // handle players trying to access this endpoint we don't hit the api from this page, so this
    // we should be able to remove this if/once we start parsing the jwt in the handle hook, at 
    // that point we can use +page.server.ts to check locals for staff user and handle accordingly
    afterNavigate(() => !userData?.is_staff && goto('/team'));
</script>

<svelte:head><title>Trivia Mafia | Host or Play</title></svelte:head>

{#if userData?.is_staff}
    <h1>Greetings {userData?.username || ''}</h1>

    <h3>Do you want to:</h3>

    <!-- NOTE: rel="external" here ensures that the layout load will run and we get our data from the api -->
    <a class="button button-red" id="host" href="/host/event-setup" rel="external">Host A Game</a>
    <a class="button button-black" id="play" href="/team">Play Trivia</a>

    <small>To view the recent changes in the application, click Here.</small>
{/if}

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