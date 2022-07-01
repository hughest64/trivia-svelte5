<script context="module" lang="ts">
	import { checkStatusCode, getFetchConfig } from '$lib/utils';
	import { get } from 'svelte/store';
	import { userdata, useractiveteam } from '$stores/user';
	import type { Load } from '@sveltejs/kit';
	const apiHost = import.meta.env.VITE_API_HOST;
    
	export const load: Load = async ({ fetch, url }) => {
        const data = get(userdata);
        
		if (!data) {
            const fetchConfig = getFetchConfig("GET")
            const response = await fetch(`${apiHost}/userteams/`, fetchConfig);
            
			if (response.ok) {
                userdata.set(await response.json());
                
            } else {   
                return checkStatusCode(response, url.pathname);
            }
		}

        return { status: 200 };
	};
</script>

<script lang="ts">
    import { goto } from '$app/navigation';
	import { eventDataLoaded, setEventStores } from '$stores/event';

	export let joincode: string;
	export let message: string;

	const handleJoinEvent = async () => {
		// TODO: should we post here? It's likely we'll be creating leaderboard entries here
		const fetchConfig = getFetchConfig("GET")
		const response = await fetch(`${apiHost}/event/${joincode}/`, fetchConfig);

		if (response.ok) {
			const data = await response.json();
			data &&	setEventStores(data)
			goto(`/game/${joincode}`);

		} else if (response.status === 404) {
			message = `Event with join code ${joincode} not found`
		}
	};
</script>

<h1>Enter Game Code</h1>

<p>Thanks for Playing with team {$useractiveteam?.team_name}! Enter the game code from your host to get started.</p>

<form on:submit|preventDefault={handleJoinEvent}>
	{#if message}<p class="error">{message}</p>{/if}
	<!-- TODO: on:focus, clear the message -->
	<div class="input-element">
		<input type="text" placeholder="Enter Code" bind:value={joincode} />
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
