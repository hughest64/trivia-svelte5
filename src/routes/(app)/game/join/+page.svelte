<script lang="ts">
    import { page } from '$app/stores';
    import type { UserData } from '$lib/types';
    import type { ActionData } from './$types';

    export let form: ActionData;
    export let joincode: string;

    const userData: UserData = $page.data?.user_data;
    $: activeTeam = userData?.teams.find((team) => team.id === userData?.active_team_id);

</script>

<svelte:head><title>Trivia Mafia | Join</title></svelte:head>

<h1>Enter Game Code</h1>

<!-- TODO: handle no activeteam, probably at a higher level, but a user
should not be able to access any endpoint here or after without an active team -->
<p>Thanks for Playing with team {activeTeam?.name}! Enter the game code from your host to get started.</p>

<form action="?/joinevent" method="POST">
    {#if form?.error}<p class="error">{form?.error}</p>{/if}
    <div class="input-element">
        <input type="text" name="joincode" placeholder="Enter Code" bind:value={joincode} />
    </div>
    <button class="button button-red" type="submit">Join Game!</button>
</form>

<style>
    h1 {
        margin: 1em;
    }
    p {
        margin: 0 1em 1em;
    }
</style>
