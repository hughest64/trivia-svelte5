<script context="module" lang="ts">
    import { checkStatusCode, getFetchConfig } from '$lib/utils';
    import type { Load } from '@sveltejs/kit';
    import type { GameSelectData, LocationSelectData, HostSelectData } from '$lib/types'
    const apiHost = import.meta.env.VITE_API_HOST
    
    export const load: Load = async({ fetch }) => {
        const fetchConfig = getFetchConfig("GET")
        const response = await fetch(`${apiHost}/eventsetup/`, fetchConfig) 

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
        // TODO: verify 401 handles properly (redirect to /)
        return checkStatusCode(response)

    }
</script>

<script lang="ts">
    import { goto } from '$app/navigation'
    import { setEventStores } from '$stores/event'

    export let gameSelectData: GameSelectData[]
    export let locationSelectData: LocationSelectData[]
    export let message: string;

    let selectLocation: LocationSelectData // TODO: set to the host's "home" location
    let selectedGame: GameSelectData

    // TODO: csrf validation
    const handleEventSubmit = async () => {
        const fetchConfig = getFetchConfig('POST', {
            location_id: selectLocation.location_id,
            game_id: selectedGame.game_id
        })

        const response = await fetch (`${apiHost}/eventsetup/`, fetchConfig)
        if (response.ok) {
            const data = await response.json()
            const joincode = data.join_code
            data && setEventStores(data)
            goto(`/host/${joincode}`)

        } else {
            message = 'Oops! Something went wrong!'
        }
    }

</script>
<h1>Choose an Event</h1>

<form class="container" on:submit|preventDefault={handleEventSubmit}>
    <h2>Locations</h2>
    {#if message}<p class="error">{message}</p>{/if}
	<!-- TODO: on:focus, clear the message -->
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