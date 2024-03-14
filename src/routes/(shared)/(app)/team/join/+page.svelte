<script lang="ts">
    import { page } from '$app/stores';

    let { form } = $props();
    const paswordParam = $page.url.searchParams.get('password');

    const next = $page.url.searchParams.get('next');
    const qp = next ? `?next=${next}` : '';

    const teamToJoin = $page.data.team_to_join;
</script>

<svelte:head><title>TriviaMafia | Join Team</title></svelte:head>

<main class="short">
    <h2>Join a Team!</h2>
    {#if paswordParam && teamToJoin}
        <h2>Team: {teamToJoin.name}</h2>
        <h4>Team Members:</h4>
        <ul>
            {#each teamToJoin?.members || [] as member}
                <li>{member}</li>
            {/each}
        </ul>
    {:else if paswordParam}
        <h4>Sorry, we couldn't find a team with that password</h4>
    {/if}
    <form action={'?/joinTeam' + qp} method="POST">
        {#if form?.error}<p class="error">{form?.error}</p>{/if}
        <div class="input-container">
            <input type="text" name="team_password" required value={paswordParam || ''} />
            <label for="team_password">Team Password</label>
        </div>
        <button class="button button-primary" type="submit" id="team-password-submit">Join Team</button>
    </form>
</main>
