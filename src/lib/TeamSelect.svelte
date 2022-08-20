<script lang="ts">
    import { getFetchConfig } from '$lib/utils';
    import { goto } from '$app/navigation';
    import { userdata, useractiveteam, type UserTeam } from '$stores/user';
    import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

    let hidecreateteam = true;
    let hideteampassword = true;

    // TODO: finish create a team and join by code (team password)
    let selected: UserTeam = $useractiveteam || $userdata?.teams[0];
    let message: string;

    const handleTeamSelectSubmit = async () => {
        if (selected.id === $userdata.active_team_id) {
            goto('/game/join');

        } else {
            const fetchConfig = getFetchConfig('POST', { team_id: selected.id });
            const response = await fetch(`${apiHost}/teamselect/`, fetchConfig);

            if (response.ok) {
                const active_team_id = await response.json();
                userdata.update((data) => ({ ...data, ...active_team_id }));
                goto('/game/join');

            } else {
                message = 'Oop! Something went wrong! Please try again.';
            }
        }
    };
</script>

<svelte:head><title>TriviaMafia | Team Select</title></svelte:head>

<h1>Create a New Team</h1>

<button class="button button-red" class:disabled={!hidecreateteam} on:click={() => (hidecreateteam = !hidecreateteam)}>
    Create a New Team
</button>

<form class:hidecreateteam on:click|preventDefault>
    <h3>Enter Your Team Name</h3>
    <div class="input-element">
        <input type="text" placeholder="Team Name" />
    </div>
    <input class="button button-white" type="submit" name="" id="" value="Submit" />
</form>

<h1>Or Play with an Existing Team</h1>

{#if $userdata?.teams.length > 0}
    <form on:submit|preventDefault={handleTeamSelectSubmit}>
        {#if message}<p class="error">{message}</p>{/if}
        <!-- TODO: on:focus, clear the message -->
        <label class="select-label" for="team-select">Choose A Team</label>
        <select class="select" id="team-select" name="team-select" bind:value={selected}>
            <!-- TODO: Team component to replicate the existing team select -->
            {#each $userdata.teams as team (team.id)}
                <option value={team}>{team.name}</option>
            {/each}
        </select>
        <input class="button button-red" type="submit" id="team-select-submit" value="Choose This Team" />
    </form>
{/if}

<button
    class="button button-black"
    class:disabled={!hideteampassword}
    on:click={() => (hideteampassword = !hideteampassword)}
>
    Enter Team Password
</button>

<form class:hideteampassword on:click|preventDefault>
    <div class="input-element">
        <input type="text" name="team-password" placeholder="Team Password" />
    </div>
    <input class="button button-white" type="submit" name="" id="team-password-submit" value="Submit" />
</form>

<style lang="scss">
    form {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    .input-element {
        width: 100%;
    }
    h1,
    h3 {
        margin: 0.5em;
    }
    select {
        margin-bottom: 1em;
    }
    .select-label {
        margin-top: 1em;
    }
    .hidecreateteam {
        display: none;
    }
    .hideteampassword {
        display: none;
    }
</style>
