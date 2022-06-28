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

	export const load: Load = async ({ fetch, params }) => {
		// TODO: deprecate eventData, check other data
		let data = get(eventData);
		if (!data) {
			const fetchConfig = getFetchConfig("GET")
			const response = await fetch(`${apiHost}/event/${params.joincode}/`, fetchConfig);

			if (response.ok) {
				data = await <EventData>response.json();
			} else {
				return checkStatusCode(response)
			}
		}
		if (data) {
			roundNumbers.set(data.rounds.map((round) => round.round_number));
			currentRoundNumber.set(data.current_round_number);
			currentQuestionNumber.set(data.current_question_number);
			eventRounds.set(data.rounds);
		}

		return { status: 200 };
	};
</script>

<script lang="ts">
	// create socket connection here?
	// then close the client in an onDestroy?
</script>

 <slot />