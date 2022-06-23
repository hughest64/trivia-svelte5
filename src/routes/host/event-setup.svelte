<script context="module" lang="ts">
    import { browser } from '$app/env'
    import type { Load } from '@sveltejs/kit';
    import type { GameSelectData, LocationSelectData, HostSelectData } from '$lib/types'
    const apiHost = import.meta.env.VITE_API_HOST

    // TODO: 
    // should this be in a get function in an endpoint file?
    // handle direct navigation
    // hanlde non-staff users (redirect)
    
    export const load: Load = async({ fetch }) => {
        // if (browser) return { status: 200 }

        const response = await fetch(
            `${apiHost}/eventsetup/`,
            {
                credentials: 'include',
                headers: {
                    accept: 'application/json'
                }
            }
        ) 
        if (response.ok) {
            const data = await <HostSelectData>response.json()

            return {
                status: 200,
                props: {
                    gameSelectData: data.game_select_data || [],
                    locationSelectData: data.location_select_data || []
                }
            }
        }
        // TODO: actually check for a 4xx code
        // not a staff user
        return {
            redirect: '/',
            status: 302
        }

    }
</script>

<script lang="ts">
    import { goto } from '$app/navigation'

    export let gameSelectData: GameSelectData[]
    export let locationSelectData: LocationSelectData[]

    let selectLocation: LocationSelectData
    let selectedGame: GameSelectData

    const handleEventSubmit = async () => {
        console.log(`Starting Event at ${selectLocation.location_name} with game ${selectedGame.game_title}`)
        // TODO: just post to /event?
        const response = await fetch (
            `${apiHost}/eventsetup/`,
            {
                method: 'POST',
                credentials: 'include',
                headers: {
                    accept: 'application/json'
                },
                body: JSON.stringify({
                    location_id: selectLocation.location_id,
                    game_id: selectedGame.game_id
                })
            }
        )
        if (response.ok) {
            // TODO set event data store
            // goto host/
        }
    }

</script>
<h1>Choose an Event</h1>

<form class="container" on:submit|preventDefault={handleEventSubmit}>
    <h2>Locations</h2>
    <select bind:value={selectLocation}>
        {#each locationSelectData as location (location.location_id)}
            <option value={location}>{location.location_name}</option>
        {/each}
    </select>
    <h2>Games</h2>
    <select bind:value={selectedGame}>
        {#each gameSelectData as game (game.game_id)}
            <option value={game}>{game.game_title}</option>
        {/each}
    </select>
    <input type="submit" name="submit" id="submit" value="Begin Event">
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