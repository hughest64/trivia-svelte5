<script context="module" lang="ts">
	import { get } from 'svelte/store';
	import {
		eventData,
		currentRoundNumber,
		currentQuestionNumber,
		eventRounds,
		roundNumbers
	} from '$stores/event';
	import type { EventData } from '$stores/event';
	import type { Load } from '@sveltejs/kit';

	// conditonally fetch event data if the event store is empty
	export const load: Load = async ({ fetch, params }) => {
		let data = get(eventData);
		if (!data) {
			const response = await fetch(`http://localhost:8000/event/${params.joincode}/`, {
				credentials: 'include',
				headers: { accept: 'application/json' }
			});

			if (response.status === 200) {
				data = await response.json() as EventData;
			} else if (response.status === 404) {
				// TODO:
				// redirect to /game-select with a not found message?
			} else if (response.status === 403) {
				return {
					// TODO: query string ?next=/game/${params.joincode}
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
</script>

<slot />
