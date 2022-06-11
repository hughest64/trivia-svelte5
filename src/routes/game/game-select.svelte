<script lang="ts">
    import { goto } from '$app/navigation'

    export let joincode: string;

    const handleJoinGame = async () => {
        console.log('you are submitting joincode', joincode)
        // post to the api to verify the code is good
        const response = await fetch (
            'http:localhost:8000/event/',
            {
                // method: 'POST',
                credentials: 'include',
                body: JSON.stringify({ joincode })
            }
        )
        // if resp.ok, set event data in a store and goto /game/[joincode]
        if (response.ok) {
            goto(`/game/${joincode}`) 
        }
        // else notify user of bad code
    }

</script>

<h1>Game Select</h1>

<form class="container" on:click|preventDefault={handleJoinGame}>
    <h2>Enter Game Code</h2>
    <input type="text" bind:value={joincode}>
    <input type="submit">
</form>

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