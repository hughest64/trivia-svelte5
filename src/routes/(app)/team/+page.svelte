<script lang="ts">
    import { page } from '$app/stores';
    import type { UserData } from '$lib/types';
    import type { ActionData } from './$types';

    export let form: ActionData;
    let hidecreateteam = true;
    let hideteampassword = true;

    const userData = <UserData>$page.data?.user_data;
</script>

<svelte:head><title>TriviaMafia | Team Select</title></svelte:head>

<h1>Create a New Team</h1>

<button class="button button-red" class:disabled={!hidecreateteam} on:click={() => (hidecreateteam = !hidecreateteam)}>
    Create a New Team
</button>

<form class:hidecreateteam on:submit|preventDefault>
    <h3>Enter Your Team Name</h3>
    <div class="input-element">
        <input type="text" placeholder="Team Name" />
    </div>
    <input class="button button-white" type="submit" name="" id="" value="Submit" />
</form>

<h1>Or Play with an Existing Team</h1>

{#if userData?.teams.length > 0}
<form method='POST'>
    {#if form?.error}<p class="error">{form?.error}</p>{/if}
    
    <label class="select-label" for="team-select">Choose A Team</label>
    <select class="select" id="team-select" name="selectedteam">
        {#each userData.teams as team (team.id)}
            <option value={team.id}>{team.name}</option>
        {/each}
    </select>
    <input type="hidden" name="currentteam" value={userData?.active_team?.id}>
    <button class="button button-red" type="submit" id="team-select-submit">Choose This Team</button>
</form>
{/if}

<button
    class="button button-black"
    class:disabled={!hideteampassword}
    on:click={() => (hideteampassword = !hideteampassword)}
>
    Enter Team Password
</button>

<form class:hideteampassword on:submit|preventDefault>
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
