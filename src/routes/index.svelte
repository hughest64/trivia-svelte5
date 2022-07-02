<script context="module" lang="ts">
	import { browser } from '$app/env';
	import { checkStatusCode, getFetchConfig } from '$lib/utils';
	import { get } from 'svelte/store';
	import { userdata } from '$stores/user';
	import type { Load } from '@sveltejs/kit';
	const apiHost = import.meta.env.VITE_API_HOST

	export const load: Load = async () => {
		const data = get(userdata)
		// if (!data && browser) {
		if (!data) {
			const fetchConfig = getFetchConfig("GET")
			const response = await fetch(`${apiHost}/user/`, fetchConfig);
	
			if (response.ok) {
				const user_data = (await response.json());
				user_data && userdata.set(user_data);
	
			} else {
				return checkStatusCode(response)
			}
		}
		return { status: 200 };
	};
</script>

<script lang="ts">
	import { goto } from '$app/navigation';
	import HostChoice from '$lib/HostChoice.svelte';
	import TeamSelect from '$lib/TeamSelect.svelte';

	let hostchoice = 'choose'; // or 'play' or 'host'

	const handleChoiceClick = (event: MouseEvent) => {
		const target = <HTMLButtonElement>event.target;
		const id = target.id;
		if (id === 'host') {
			goto('/host/event-setup');
		}
		if (id === 'play') {
			hostchoice = 'play';
			goto('/');
		}
	};

	let historyIndex = 0;
	const handlepopstate = (event: PopStateEvent) => {
		const eventIndex = event.state['sveltekit:index'] || 0

		// back
		if (historyIndex === 0 || eventIndex < historyIndex) {
			hostchoice = 'choose'

		// forward
		} else if (historyIndex !== 0 && eventIndex > historyIndex) {
			hostchoice = 'play'
		}
		historyIndex = eventIndex
	};
</script>

<svelte:window on:popstate={handlepopstate} />

{#if ($userdata?.username && !$userdata?.is_staff) || hostchoice === 'play'}
	<TeamSelect />
{:else}
	<HostChoice on:click={handleChoiceClick} />
{/if}
