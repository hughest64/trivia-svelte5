<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import type { UserData } from '$lib/types';
    import type { ActionData } from './$types';

    export let form: ActionData;

    const userData = getStore<UserData>('userData');
    $: activeTeam = $userData?.teams.find((team) => team.id === $userData?.active_team_id);

    const errorMessageMap: Record<string, string> = {
        join_required: 'Please Join an event by entering the join code',
        player_limit_excedded: `Someone from ${
            activeTeam ? activeTeam.name : 'your team'
        } has alredy joined this event`,
        none: ''
    };
    $: errMsg = errorMessageMap[$page.url.searchParams.get('reason') || 'none'];
</script>

<svelte:head><title>Trivia Mafia | Join</title></svelte:head>

<h1>Enter Game Code</h1>

{#if !!userData}
    <p>Thanks for Playing with team {activeTeam?.name}! Enter the game code from your host to get started.</p>
{/if}
{#if errMsg}
    <p>{errMsg}</p>
{/if}

<form action="?/joinevent" method="POST">
    {#if form?.error}<p class="error">{form?.error}</p>{/if}
    <div class="input-element">
        <input type="text" name="joincode" placeholder="Enter Code" autocapitalize="none" autocomplete="off" />
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
