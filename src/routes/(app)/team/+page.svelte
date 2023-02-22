<script lang="ts">
    import { getStore } from '$lib/utils';
    import type { UserData } from '$lib/types';
    import type { ActionData } from './$types';

    export let form: ActionData;
    let hidecreateteam = true;
    let hideteampassword = true;

    const userData = getStore<UserData>('userData');
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

    <form action="?/createTeam" method="POST" class:hidecreateteam on:submit|preventDefault>
        <h3>Enter Your Team Name</h3>
        <div class="input-container">
            <input type="text" name="team_name" required />
            <label for="team_name">Team Name</label>
        </div>
        <input class="button button-tertirary" type="submit" id="team-create-submit" value="Submit" />
    </form>

    <h1>Or Play with an Existing Team</h1>

    {#if $userData?.teams.length > 0}
        <form action="?/selectTeam" method="POST">
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

    <form action="?/submitTeamPassword" method="POST" class:hideteampassword on:submit|preventDefault>
        <div class="input-container">
            <input type="text" name="team_password" required />
            <label for="team_password">Team Password</label>
        </div>
        <input class="button button-white" id="team-password-submit" value="Submit" />
    </form>
</main>

<style lang="scss">
    .hidecreateteam {
        display: none;
    }
    .hideteampassword {
        display: none;
    }
</style>
