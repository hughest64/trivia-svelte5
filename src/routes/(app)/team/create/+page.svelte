<script lang="ts">
    import { slide, fly } from 'svelte/transition';
    import { page } from '$app/stores';
    import { enhance } from '$app/forms';

    $: form = $page.form;
    $: teamName = form?.team_name;
    $: teamPass = form?.team_password;
    $: qr = form?.qr;

    $: next = $page.url.searchParams.get('next');
    $: qp = next ? `&next=${next}` : '';
</script>

<svelte:head><title>TriviaMafia | Create Team</title></svelte:head>

<main class="short">
    {#if !teamName}
        <div class="flex-column full-width" out:slide>
            <form action={'?/createTeam' + qp} method="POST" transition:slide use:enhance>
                <h2 class="form-header">Choose a Team Name</h2>
                {#if form?.error}<p class="error">{form?.error}</p>{/if}
                <div class="input-container">
                    <input type="text" name="team_name" required />
                    <label for="team_name">Team Name</label>
                </div>
                <button class="button button-primary" id="team-create-submit">Submit</button>
            </form>
            <a class="join-link" href="join">Join an existing team (password required)</a>
        </div>
    {:else}
        <div class="flex-column full-width" in:fly={{ y: 500, duration: 1000 }}>
            <h1>Welcome</h1>
            <h3>{teamName}</h3>
            <div class="line" />
            <h3>Team Password:</h3>
            <h3>{teamPass}</h3>
            <!-- TODO: check that it exists and use a sensible fallback -->
            {@html qr}
            <a href="/game/join" class="button button-primary" data-sveltekit-reload>Next</a>
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
    .line {
        margin: 2rem 0;
        width: min(20rem, calc(100% - 1rem));
        height: 1px;
        background-color: var(--color-secondary);
    }
</style>
