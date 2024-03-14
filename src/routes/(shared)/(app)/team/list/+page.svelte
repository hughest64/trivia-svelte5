<script lang="ts">
    import { page } from '$app/stores';
    import { getState } from '$lib/state/utils.svelte';

    let { form } = $props();

    let userData = getState('userState');
    const next = $page.url.searchParams.get('next');
    const qp = next ? `&next=${next}` : '';
</script>

<svelte:head><title>TriviaMafia | Team List</title></svelte:head>

<main class="short">
    {#if userData?.teams?.length > 0}
        <h1>Teams you've joined:</h1>

        <form action={'?/selectTeam' + qp} method="POST">
            {#if form?.error}<p class="error">{form?.error}</p>{/if}

            <label class="select-label" for="team-select">Choose A Team</label>
            <select class="select" id="team-select" name="selectedteam">
                {#each userData.teams as team (team.id)}
                    <option value={team.id}>{team.name}</option>
                {/each}
            </select>
            <input type="hidden" name="currentteam" value={userData?.active_team_id} />

            <a class="join-link" href="join">Join an existing team (password required)</a>

            <button class="button button-primary" type="submit" id="team-select-submit">Let's Play!</button>
        </form>
        <h2 class="spacer">- or -</h2>
    {:else}
        <h2>It looks like you don't have any teams!</h2>
        <a class="join-link" href="join">Join a existing team (password required)</a>
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
