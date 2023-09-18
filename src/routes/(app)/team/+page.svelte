<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';

    const userData = getStore('userData');
    const activeTeam = $userData.teams.find((t) => t.id === $userData.active_team_id);
    const queryString = $page.url.search;
    const next = $page.url.searchParams.get('next') || 'game/join';
    $: console.log(queryString);
</script>

<main class="short">
    <h1>Welcome!</h1>

    <h2>You are currently playing with team:</h2>

    <h3>{activeTeam?.name}</h3>

    <a class="button button-primary" href={next} data-sveltekit-reload>Looks good, let's go!</a>

    <a class="team-select-link" href="/team/list{queryString}">Play with a different team</a>
</main>

<style lang="scss">
    .team-select-link {
        font-style: italic;
    }
    h2,
    h3 {
        margin: 2rem auto;
    }
</style>
