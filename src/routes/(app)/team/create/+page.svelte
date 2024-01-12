<script lang="ts">
    import { slide, fly } from 'svelte/transition';
    import { page } from '$app/stores';
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';

    // TODO: qr code handling, probably in python like this:
    // https://www.twilio.com/blog/generate-qr-code-with-python
    // it uses this https://pypi.org/project/qrcode/
    // and maybe we store an svg at a team table attritute, or
    // maybe we store the image on 1pg.us and store the url on the team?

    $: form = $page.form;
    $: teamName = form?.teamName || 'Remove This Default';
    $: teamPass = form?.teamPass || 'not-the-password';
    $: console.log(form);

    const userData = getStore('userData');
    const hasTeams = $userData.teams?.length > 0;
    const isGuest = $userData.is_guest;

    $: next = $page.url.searchParams.get('next');
    $: qp = next ? `&next=${next}` : '';
    let showForm = hasTeams;
</script>

<svelte:head><title>TriviaMafia | Create Team</title></svelte:head>

<main class="short">
    {#if !teamName}
        <div class="flex-column full-width" out:slide>
            {#if !hasTeams && !isGuest}
                <h2 class="form-header">It looks like you don't have any teams yet</h2>
                <a class="join-link" href="join">Join an existing team (password required)</a>
                <h2 class="form-header">- or -</h2>
                <button class="button button-primary" on:click={() => (showForm = !showForm)}>Create New Team</button>
            {/if}
            {#if showForm}
                <form action={'?/createTeam' + qp} method="POST" transition:slide use:enhance>
                    <h2 class="form-header">Choose a Team Name</h2>
                    {#if form?.error}<p class="error">{form?.error}</p>{/if}
                    <div class="input-container">
                        <input type="text" name="team_name" required />
                        <label for="team_name">Team Name</label>
                    </div>
                    <button class="button button-primary" id="team-create-submit">Submit</button>
                </form>
            {/if}
        </div>
    {:else}
        <div class="flex-column full-width" in:fly={{ y: 500, duration: 1000 }}>
            <h1>Welcome</h1>
            <h3>{teamName}</h3>
            <hr />
            <h3>Team Password:</h3>
            <h3>{teamPass}</h3>

            <a href="game/join" class="button button-primary">Next</a>
        </div>
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
    hr {
        margin: 2rem 0;
        width: var(--max-element-width);
        border: 1px solid var(--color-secondary);
    }
</style>
