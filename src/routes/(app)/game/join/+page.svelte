<script lang="ts">
    import { userdata, useractiveteam } from '$stores/user';
    import type { ActionData } from './$types';

    export let form: ActionData;
    export let joincode: string;

</script>

<svelte:head><title>Trivia Mafia | Join</title></svelte:head>

<h1>Enter Game Code</h1>

<!-- TODO: handle no activeteam -->
<p>{$userdata?.username},</p>
<p>Thanks for Playing with team {$useractiveteam?.name}! Enter the game code from your host to get started.</p>

<form action="?/joinevent" method="POST">
    {#if form?.error}<p class="error">{form?.error}</p>{/if}
    <div class="input-element">
        <input type="text" name="joincode" placeholder="Enter Code" bind:value={joincode} />
    </div>
    <input class="button button-red" type="submit" value="Join Game!" />
</form>

<style>
    h1 {
        margin: 1em;
    }
    p {
        margin: 0 1em 1em;
    }
</style>
