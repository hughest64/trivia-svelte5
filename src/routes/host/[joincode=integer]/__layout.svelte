 <script context="module" lang="ts">
	import { checkStatusCode, getFetchConfig } from '$lib/utils';
	import { get } from 'svelte/store';
	import { setEventStores, eventDataLoaded } from '$stores/event';
	import type { EventData } from '$lib/types';
	import type { Load } from '@sveltejs/kit';
	const apiHost = import.meta.env.VITE_API_HOST;

	export const load: Load = async ({ fetch, params }) => {
		// TODO: deprecate eventData, check other data

		if (!get(eventDataLoaded)) {
			const fetchConfig = getFetchConfig("GET")
			const response = await fetch(`${apiHost}/event/${params.joincode}/`, fetchConfig);

			if (response.ok) {
				const data = await <EventData>response.json();
				data && setEventStores(data)
			} else {
				return checkStatusCode(response)
			}
		}
		return { status: 200 };
	};
</script>

<script lang="ts">
	// create socket connection here?
	// then close the client in an onDestroy?
</script>

 <slot />