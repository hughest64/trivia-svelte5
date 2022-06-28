<script context="module" lang="ts">
	import { checkStatusCode, getFetchConfig } from '$lib/utils';
	import { get } from 'svelte/store';
	import {
		eventData,
		currentRoundNumber,
		currentQuestionNumber,
		eventRounds,
		roundNumbers
	} from '$stores/event';
	import type { EventData } from '$lib/types';
	import type { Load } from '@sveltejs/kit';
	const apiHost = import.meta.env.VITE_API_HOST;

	export const load: Load = async ({ fetch, url, params }) => {
		// TODO: check some other data, as we should deprecate eventData
		let data = get(eventData);
		if (!data) {
			const fetchConfig = getFetchConfig("GET")
            const response = await fetch(`${apiHost}/event/${params.joincode}/`, fetchConfig);

			if (response.ok) {
				data = (await response.json()) as EventData;
			} else {
				return checkStatusCode(response, url.pathname)
			}
		}
		if (data) {
			// TODO: we shouldn't need to set eventData
			eventData.set(data)
			roundNumbers.set(data.rounds.map((round) => round.round_number));
			currentRoundNumber.set(data.current_round_number);
			currentQuestionNumber.set(data.current_question_number);
			eventRounds.set(data.rounds);
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
