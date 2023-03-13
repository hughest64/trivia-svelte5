<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';

    $: form = $page.form;
    const userData = getStore('userData');
    $: activeTeam = $userData?.teams.find((team) => team.id === $userData?.active_team_id);
</script>

<svelte:head><title>Trivia Mafia | Join</title></svelte:head>

<main class="short">
    <h1>Enter Game Code</h1>

    {#if !!userData}
        <p>Thanks for Playing with team {activeTeam?.name}! Enter the game code from your host to get started.</p>
    {/if}

    <form action="?/joinevent" method="POST">
        {#if form?.error}<p class="error">{form?.error}</p>{/if}
        <div class="input-container">
            <input type="text" name="joincode" id="joincode" autocapitalize="none" autocomplete="off" required />
            <label for="joincode">Enter Code</label>
        </div>
        <button class="button button-primary" type="submit">Join Game!</button>
    </form>
</main>
