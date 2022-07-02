<script context="module" lang="ts">
    import { browser } from '$app/env';

    import { userdata } from '$stores/user';
    import { checkStatusCode, getFetchConfig } from '$lib/utils';

    import type { Load } from '@sveltejs/kit';
    import type { GameSelectData, LocationSelectData } from '$lib/types'

    const apiHost = import.meta.env.VITE_API_HOST
    
    export const load: Load = async({ fetch }) => {
        if (!browser) {
            return { status: 200}
        }
        const fetchConfig = getFetchConfig("GET")
        const response = await fetch(`${apiHost}/eventsetup/`, fetchConfig) 

        if (response.ok) {
            const data = await response.json()
            data && userdata.set(data.user_data);

            return {
                status: 200,
                props: {
                    gameSelectData: data.game_select_data || [],
                    locationSelectData: data.location_select_data || []
                }
            }
        }
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
            message = 'Oops! Something went wrong! Please try again.'
        }
    }

</script>

<svelte:head><title>Trivia Mafia | Event Setup</title></svelte:head>

<h1>Choose a Trivia Event</h1>

<form on:submit|preventDefault={handleEventSubmit}>
    {#if message}<p class="error">{message}</p>{/if}
	<!-- TODO: on:focus, clear the message -->
    
    <label class="select-label" for="game-select">Choose your Game</label>
    <select class="select" name="game-select" id="game-select" bind:value={selectedGame}>
        {#each gameSelectData as game (game.game_id)}
            <option value={game}>{game.game_title}</option>
        {/each}
    </select>

    <label for="loaction-select" class="select-label">Choose your Venue</label>
    <select class="select" name="location-select" id="location-select" bind:value={selectLocation}>
        {#each locationSelectData as location (location.location_id)}
            <option value={location}>{location.location_name}</option>
        {/each}
    </select>

    <input class="button button-red" type="submit" name="submit" id="submit" value="Begin Event">
</form>

<style>
    form {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
	}
    h1 {
		margin: 1em 0;
	}
	select {
		margin-bottom: 2em;
	}
	.select-label {
		margin-top: 1em;
        width: 100%;
	}
</style>