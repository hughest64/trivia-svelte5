<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';

    $: form = $page.form;
    const userData = getStore('userData');
    $: activeTeam = $userData?.teams.find((team) => team.id === $userData?.active_team_id);
</script>

<svelte:head><title>Trivia Mafia | Join</title></svelte:head>

<main class="short">
    {#if !!userData}
        <h1 class="team-header">Team</h1>
        <h2>{activeTeam?.name}</h2>
        <div class="line" />
    {/if}

    <h1>Enter Game Code</h1>

    <form action="?/joinevent" method="POST">
        {#if form?.error}<p class="error">{form?.error}</p>{/if}
        <div class="input-container">
            <input type="text" name="joincode" id="joincode" autocapitalize="none" autocomplete="off" required />
            <label for="joincode">Game Code</label>
        </div>
        <button class="button button-primary" type="submit">Join Game!</button>
    </form>
</main>

<style lang="scss">
    .team-header {
        margin-bottom: 0;
    }
    .line {
        height: 2px;
        width: min(30rem, calc(100% - 1rem));
        margin: 1rem 0 2rem;
        background-color: var(--color-primary);
    }
</style>
