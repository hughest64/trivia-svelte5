<script lang="ts">
    import { setEventStores } from '$stores/event';
    import { getFetchConfig } from '$lib/utils';
    import { useractiveteam } from '$stores/user';
    import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

    export let joincode: string;
    export let message: string;

    const handleJoinEvent = async () => {
        // TODO: should we post here? It's likely we'll be creating leaderboard entries here
        const fetchConfig = getFetchConfig('GET');
        const response = await fetch(`${apiHost}/event/${joincode}/`, fetchConfig);

        if (response.ok) {
            const data = await response.json();
            data && setEventStores(data);
            window.open(`/game/${joincode}`, '_self');
        } else if (response.status === 404) {
            message = `Event with join code ${joincode} not found`;
        }
    };
</script>

<svelte:head><title>Trivia Mafia | Join</title></svelte:head>

<h1>Enter Game Code</h1>

<p>Thanks for Playing with team {$useractiveteam?.name}! Enter the game code from your host to get started.</p>

<form on:submit|preventDefault={handleJoinEvent}>
    {#if message}<p class="error">{message}</p>{/if}
    <!-- TODO: on:focus, clear the message -->
    <div class="input-element">
        <input type="text" name="joincode" placeholder="Enter Code" bind:value={joincode} />
    </div>
    <input class="button button-red" type="submit" value="Join Game!" />
</form>

<style>
    h1 {
        margin: 1em;
    }
    p {
        margin: 0 1em 1em;
    }
</style>
