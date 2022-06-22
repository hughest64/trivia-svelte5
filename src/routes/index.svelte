<script context="module" lang="ts">
	import { userdata, userteams } from '$stores/user';
	import type { Load } from '@sveltejs/kit';
	const apiHost = import.meta.env.VITE_API_HOST

	export const load: Load = async ({ fetch }) => {
		// if (!browser) return { status: 200 };

		const response = await fetch(
			// TODO: store the host portion of the url in env
			// if dev use localhost, if prod use ...
			`${apiHost}/userteams/`,
			{
				headers: { accept: 'application/json' },
				credentials: 'include'
			}
		);

		if (response.ok) {
			const { user_teams, user_data } = (await response.json()) || {};
			userdata.set({ ...user_data });
			userteams.set([...user_teams]);

			return {
				status: 200
			};
		}

		return {
			redirect: '/user/login',
			status: 302
		};
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

	// TODO: onMount goto /user/login if no user data ?
</script>

<svelte:window on:popstate={handlepopstate} />

{#if ($userdata.username && !$userdata.is_staff) || hostchoice === 'play'}
	<TeamSelect />
{:else}
	<HostChoice on:click={handleChoiceClick} />
{/if}
