<script context="module" lang="ts">
	import { checkStatusCode, getFetchConfig } from '$lib/utils';
	import { get } from 'svelte/store';
	import { userdata } from '$stores/user';
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

<h1>Game Select</h1>

<form class="container" on:submit|preventDefault={handleJoinEvent}>
	<h2>Enter Game Code</h2>
	{#if message}<p class="error">{message}</p>{/if}
	<!-- TODO: on:focus, clear the message -->
	<input type="text" bind:value={joincode} />
	<input type="submit" value="Join The Event" />
</form>

<style>
	.container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		gap: 0.75em;
		max-width: 30rem;
		margin: 5rem auto 0;
	}
</style>
