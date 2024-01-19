<script lang="ts">
    import { page } from '$app/stores';

    $: form = $page.form;
    const paswordParam = $page.url.searchParams.get('password');

    $: next = $page.url.searchParams.get('next');
    $: qp = next ? `?next=${next}` : '';
</script>

<svelte:head><title>TriviaMafia | Join Team</title></svelte:head>

<main class="short">
    <h1>Join a Team!</h1>
    <form action={'?/joinTeam' + qp} method="POST">
        {#if form?.error}<p class="error">{form?.error}</p>{/if}
        <div class="input-container">
            <input type="text" name="team_password" required value={paswordParam || ''} />
            <label for="team_password">Team Password</label>
        </div>
        <button class="button button-primary" type="submit" id="team-password-submit">Join Team</button>
    </form>
</main>
