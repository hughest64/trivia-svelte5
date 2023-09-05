<script lang="ts">
    import { slide } from 'svelte/transition';
    import { enhance } from '$app/forms';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    // import type { ActionData } from './$types';

    // TODO: handle form error (might need a bit of nesting to get it on the right form)
    // export let form: ActionData;
    $: form = $page.form;
    let hidecreateteam = true;
    let hideteampassword = true;

    const userData = getStore('userData');
    $: next = $page.url.searchParams.get('next');
    $: qp = next ? `&next=${next}` : '';
</script>

<svelte:head><title>TriviaMafia | Team Select</title></svelte:head>

<main class="short">
    <h1>Create a New Team</h1>

    <button
        class="button button-primary"
        class:disabled={!hidecreateteam}
        on:click={() => (hidecreateteam = !hidecreateteam)}
    >
        Create a New Team
    </button>

    {#key hidecreateteam}
        <form transition:slide|local class:hidecreateteam action={'?/createTeam' + qp} method="POST" use:enhance>
            {#if form?.error}<p class="error">{form?.error}</p>{/if}
            <h3>Enter Your Team Name</h3>
            <div class="input-container">
                <input type="text" name="team_name" required />
                <label for="team_name">Team Name</label>
            </div>
            <button class="button button-tertiary" id="team-create-submit">Submit</button>
        </form>
    {/key}
    <h1>Or Play with an Existing Team</h1>

    {#if $userData?.teams.length > 0}
        <form action={'?/selectTeam' + qp} method="POST">
            {#if form?.error}<p class="error">{form?.error}</p>{/if}

            <label class="select-label" for="team-select">Choose A Team</label>
            <select class="select" id="team-select" name="selectedteam">
                {#each $userData.teams as team (team.id)}
                    <option value={team.id}>{team.name}</option>
                {/each}
            </select>
            <input type="hidden" name="currentteam" value={$userData?.active_team_id} />
            <button class="button button-primary" type="submit" id="team-select-submit">Choose This Team</button>
        </form>
    {/if}

    <button
        class="button button-secondary"
        class:disabled={!hideteampassword}
        on:click={() => (hideteampassword = !hideteampassword)}
    >
        Enter Team Password
    </button>

    {#key hideteampassword}
        <form transition:slide|local class:hideteampassword action={'?/joinTeam' + qp} method="POST" use:enhance>
            <div class="input-container">
                <input type="text" name="team_password" required />
                <label for="team_password">Team Password</label>
            </div>
            <button class="button button-tertiary" type="submit" id="team-password-submit">Submit</button>
        </form>
    {/key}
</main>

<style lang="scss">
    .hidecreateteam {
        display: none;
    }
    .hideteampassword {
        display: none;
    }
</style>
