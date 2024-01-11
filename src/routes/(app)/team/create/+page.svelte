<script lang="ts">
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';

    $: form = $page.form;

    const userData = getStore('userData');
    const hasTeams = $userData.teams?.length > 0;
    const isGuest = $userData.is_guest;

    $: next = $page.url.searchParams.get('next');
    $: qp = next ? `&next=${next}` : '';
    let showForm = hasTeams;
</script>

<svelte:head><title>TriviaMafia | Create Team</title></svelte:head>

<main class="short">
    {#if !hasTeams && !isGuest}
        <h2 class="form-header">It looks like you don't have any teams yet</h2>
        <a class="join-link" href="join">Join an existing team (password required)</a>
        <h2 class="form-header">- or -</h2>
        <button class="button button-primary" on:click={() => (showForm = !showForm)}>Create New Team</button>
    {/if}
    {#if showForm}
        <form action={'?/createTeam' + qp} method="POST" transition:slide>
            <h2 class="form-header">Choose a Team Name</h2>
            {#if form?.error}<p class="error">{form?.error}</p>{/if}
            <div class="input-container">
                <input type="text" name="team_name" required />
                <label for="team_name">Team Name</label>
            </div>
            <button class="button button-primary" id="team-create-submit">Submit</button>
        </form>
    {/if}
</main>

<style lang="scss">
    .form-header {
        text-align: center;
    }
    .join-link {
        margin: 2rem auto;
        font-style: italic;
    }
</style>
