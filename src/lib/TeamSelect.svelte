<script lang="ts">
    import { userdata, userteams, type UserTeam } from '../stores/user';

    let selected: UserTeam
    // $: console.log(selected)

    const handleTeamSelectSubmit = () => {
        // post to the api and if resp.ok, goto gameselct (or next=/some/place)
        console.log("you have chosen to play with", selected.team_name)
    }
</script>

<h1>Team Select</h1>

{#if !!$userteams }
    <form class="container" on:submit|preventDefault={handleTeamSelectSubmit}>
        <h2>{$userdata.username} Select A Team</h2>
        <select bind:value={selected}>
            {#each $userteams as team (team.team_id)}
                <option value={team}>{team.team_name}</option>
            {/each}
        </select>
        <input type="submit" value="Choose This Team">
    </form>
{/if}

<style>
    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: .75em;
        max-width: 30rem;
        margin: 5rem auto 0;
    }
</style>