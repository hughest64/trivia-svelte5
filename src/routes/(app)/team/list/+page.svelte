<script lang="ts">
    import { slide } from 'svelte/transition';
    import { enhance } from '$app/forms';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';

    $: form = $page.form;

    const userData = getStore('userData');
    $: next = $page.url.searchParams.get('next');
    $: qp = next ? `&next=${next}` : '';
</script>

<svelte:head><title>TriviaMafia | Team Select</title></svelte:head>

<main class="short">
    <h1>Teams you've joined:</h1>

    {#if $userData?.teams?.length > 0}
        <form action={'?/selectTeam' + qp} method="POST" use:enhance>
            {#if form?.error}<p class="error">{form?.error}</p>{/if}

            <label class="select-label" for="team-select">Choose A Team</label>
            <select class="select" id="team-select" name="selectedteam">
                {#each $userData.teams as team (team.id)}
                    <option value={team.id}>{team.name}</option>
                {/each}
            </select>
            <input type="hidden" name="currentteam" value={$userData?.active_team_id} />

            <a class="join-link" href="join">Join a different team (password required)</a>

            <button class="button button-primary" type="submit" id="team-select-submit">Let's Play!</button>
        </form>
        <h2 class="spacer">- or -</h2>
    {/if}

    <a href="create" class="button button-primary">Create a new team</a>
</main>

<style lang="scss">
    .join-link {
        margin: 2rem auto;
        font-style: italic;
    }
    .spacer {
        margin: 2rem auto;
    }
</style>
