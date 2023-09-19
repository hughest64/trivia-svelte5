<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';

    const userData = getStore('userData');
    const activeTeam = $userData.teams.find((t) => t.id === $userData.active_team_id);
    const queryString = $page.url.search;
    const next = $page.url.searchParams.get('next') || 'game/join';
</script>

<svelte:head><title>TriviaMafia | Team</title></svelte:head>

<main class="short">
    <h1>Welcome!</h1>

    {#if activeTeam}
        <h2>You are currently playing with team:</h2>

        <h3>{activeTeam?.name}</h3>

        <a class="button button-primary" href={next} data-sveltekit-reload>Looks good, let's go!</a>
        <a class="link" href="/team/list{queryString}">Play with a different team</a>
    {:else}
        <h2>It looks like you haven't selected a team</h2>
        <a class="link" href="/team/list{queryString}">Select a team</a>
    {/if}
</main>

<style lang="scss">
    .link {
        font-style: italic;
    }
    h2,
    h3 {
        margin: 2rem auto;
    }
</style>
