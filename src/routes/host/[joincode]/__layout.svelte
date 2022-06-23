 <script context="module" lang="ts">
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

	// TODO: handle direct navigation, the event endpoint should return userdata
	// and we should make sure that a user has an active team -  will we get a 401 if we set up staff permission?

	// conditonally fetch event data if the event store is empty
	export const load: Load = async ({ fetch, params }) => {
		let data = get(eventData);
		if (!data) {
			const response = await fetch(`${apiHost}/event/${params.joincode}/`, {
				credentials: 'include',
				headers: { accept: 'application/json' }
			});

			if (response.status === 200) {
				data = (await response.json()) as EventData;
			} else if (response.status === 404) {
				// TODO:
				// redirect to /join with a not found message?
			} else if (response.status === 403) {
				return {
					// TODO: query string ?next=/host/${params.joincode}
					redirect: '/user/login',
					status: 302
				};
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