<script lang="ts">
    import { goto } from '$app/navigation'

    export let joincode: string;

    const handleJoinEvent = async () => {
        const response = await fetch (
            `http://localhost:8000/event/${joincode}/`,
            {
                credentials: 'include',
                headers: { accept: 'application/json' },
            }
        )

        if (response.ok) {
            goto(`/game/${joincode}`) 
        }
        // else notify user of bad code
    }

</script>

<h1>Game Select</h1>

<form class="container" on:submit|preventDefault={handleJoinEvent}>
    <h2>Enter Game Code</h2>
    <input type="text" bind:value={joincode}>
    <input type="submit" value="Join The Event">
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