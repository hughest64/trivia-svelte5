<script lang="ts">
    import { userdata, useractiveteam, type UserTeam } from '$stores/user';

    export let errors: Record<string, string> = {};

    let hidecreateteam = true;
    let hideteampassword = true;

    // TODO: finish create a team and join by code (team password)
    let selected: UserTeam = $useractiveteam || $userdata?.teams[0];
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
    <form action='' method='POST'>
        {#if errors?.message}<p class="error">{errors?.message}</p>{/if}
        
        <label class="select-label" for="team-select">Choose A Team</label>
        <select class="select" id="team-select" name="selectedteam" bind:value={selected.id}>
            <!-- TODO: Team component to replicate the existing team select -->
            {#each $userdata.teams as team (team.id)}
                <option value={team.id}>{team.name}</option>
            {/each}
        </select>
        <input type="hidden" name="currentteam" value={$useractiveteam?.id}>
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
