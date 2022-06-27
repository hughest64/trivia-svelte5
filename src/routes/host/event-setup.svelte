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
        const route = response.status === 401 ? '/' : '/user/login'
        return {
            redirect: route,
            status: 302
        }

    }
</script>

<script lang="ts">
    import { goto } from '$app/navigation'
    import { eventData } from '$stores/event'

    export let gameSelectData: GameSelectData[]
    export let locationSelectData: LocationSelectData[]

    let selectLocation: LocationSelectData // TODO: set to the host's "home" location
    let selectedGame: GameSelectData

    const handleEventSubmit = async () => {

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
            const data = await response.json()
            const joincode = data.join_code
            data && eventData.set(data)
            goto(`/host/${joincode}`)
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