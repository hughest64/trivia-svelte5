<script lang="ts">
    import { enhance } from '$app/forms';
    import { page } from '$app/stores';

    $: form = $page.form;

    $: next = $page.url.searchParams.get('next');
    $: qp = next ? `&next=${next}` : '';
</script>

<svelte:head><title>TriviaMafia | Create Team</title></svelte:head>

<main class="short">
    <h1>Welcome!</h1>
    <h2>Create a new team:</h2>
    <form action={'?/createTeam' + qp} method="POST">
        {#if form?.error}<p class="error">{form?.error}</p>{/if}
        <div class="input-container">
            <input type="text" name="team_name" required />
            <label for="team_name">Team Name</label>
        </div>
        <button class="button button-primary" id="team-create-submit">Submit</button>
    </form>

    <a class="join-link" href="join">Join an existing team (password required)</a>
    <a href="list" class="join-link">Show my teams</a>
</main>

<style lang="scss">
    .join-link {
        margin: 2rem auto;
        font-style: italic;
    }
</style>
