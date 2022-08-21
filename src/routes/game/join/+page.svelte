<script lang="ts">
    import { userdata, useractiveteam } from '$stores/user';
    export let errors: Record<string, string>;
    export let joincode: string;

</script>

<svelte:head><title>Trivia Mafia | Join</title></svelte:head>

<h1>Enter Game Code</h1>

<!-- TODO: handle no activeteam -->
<p>{$userdata?.username},</p>
<p>Thanks for Playing with team {$useractiveteam?.name}! Enter the game code from your host to get started.</p>

<!-- <form on:submit|preventDefault={handleJoinEvent}> -->
<form action="" method="POST">
    {#if errors.message}<p class="error">{errors.message}</p>{/if}
    <!-- TODO: on:focus, clear the message -->
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
