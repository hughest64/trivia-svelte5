<script context="module" lang="ts">
	import { get } from 'svelte/store';
	import { checkStatusCode, getFetchConfig } from '$lib/utils';
	import { eventDataLoaded, setEventStores } from '$stores/event';

	import type { EventData } from '$lib/types';
	import type { Load } from '@sveltejs/kit';

	const apiHost = import.meta.env.VITE_API_HOST;

	export const load: Load = async ({ fetch, url, params }) => {
		if (!get(eventDataLoaded)) {
			const fetchConfig = getFetchConfig("GET")
            const response = await fetch(`${apiHost}/event/${params.joincode}/`, fetchConfig);

			if (response.ok) {
				const data = (await response.json()) as EventData;
				data && setEventStores(data)
			} else {
				return checkStatusCode(response, url.pathname)
			}
		}

		return { status: 200 };
	};
</script>

<script lang="ts">
	import { page } from '$app/stores'
	const joincode = $page.params.joincode

	// create socket connection here?
	// then close the client in an onDestroy?
</script>

<svelte:head>
	<title>Trivia Mafia Event {joincode}</title>
</svelte:head>

<slot />
