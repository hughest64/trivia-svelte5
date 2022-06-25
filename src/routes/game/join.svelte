<script context="module" lang="ts">
    import { get } from 'svelte/store'
    import { userdata } from '$stores/user'
    import type { Load } from '@sveltejs/kit';

    const apiHost = import.meta.env.VITE_API_HOST

    export const load: Load = async({ fetch }) => {
        const data = get(userdata);
        if (!data) {
            const response = await fetch(
                `${apiHost}/userteams/`,
                {
                    credentials: 'include',
                    headers: { accept: 'application/json' }
                }
            )
            if (response.ok) {
                userdata.set(await response.json())
            } else {
                return {
                    redirect: '/user/login',
                    status: 302
                }
            }
        }

        return { status: 200 }
    }
</script>
<script lang="ts">
    import { goto } from '$app/navigation'
    import { eventData } from '$stores/event'

    export let joincode: string;

    const handleJoinEvent = async () => {
        const response = await fetch (
            `${apiHost}/event/${joincode}/`,
            {
                credentials: 'include',
                headers: { accept: 'application/json' },
            }
        )

        if (response.ok) {
            const data = await response.json()
            data && eventData.set(data)
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