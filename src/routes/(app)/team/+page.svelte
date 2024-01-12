<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';

    $: form = $page.form;

    const userData = getStore('userData');
    $: next = $page.url.searchParams.get('next');
    $: qp = next ? `&next=${next}` : '';
</script>

<svelte:head><title>TriviaMafia | Team List</title></svelte:head>

<main class="short">
    {#if $userData?.teams?.length > 0}
        <h1>Teams you've joined:</h1>

        <form action={'?/selectTeam' + qp} method="POST">
            {#if form?.error}<p class="error">{form?.error}</p>{/if}

            <label class="select-label" for="team-select">Choose A Team</label>
            <select class="select" id="team-select" name="selectedteam">
                {#each $userData.teams as team (team.id)}
                    <option value={team.id}>{team.name}</option>
                {/each}
            </select>
            <input type="hidden" name="currentteam" value={$userData?.active_team_id} />

            <button class="button button-primary" type="submit" id="team-select-submit">Let's Play!</button>
        </form>
    {/if}
    <a href="team/create" class="button button-primary">Create a new team</a>

    <h2>- or -</h2>

    <a class="join-link" href="team/join">Join an existing team (password required)</a>
</main>

<style lang="scss">
    .join-link {
        margin: 2rem auto;
        font-style: italic;
    }
</style>
