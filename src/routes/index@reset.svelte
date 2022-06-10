<script context="module" lang="ts">
	import { browser } from '$app/env';
	import { userdata, userteams } from '../stores/user';
	import type { Load } from '@sveltejs/kit';

	export const load: Load = async ({ fetch, session }) => {
		if (!browser) return { status: 200 };

		const response = await fetch(
			// TODO: store the host portion of the url in env
			// if dev use localhost, if prod use ...
			'http://localhost:8000/userteams/',
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
				status: 200,
			};
		}

		return {
			redirect: '/user/login',
			status: 302
		};
	};
</script>

<script lang="ts">
	import { afterNavigate, goto } from '$app/navigation';
	import HostChoice from '$lib/HostChoice.svelte';
	import TeamSelect from '$lib/TeamSelect.svelte';

	let hostchoice = 'choose' // or 'play' or 'host'
	$: hostchoice === 'host' && goto('/host/event-setup')
	$: hostchoice === 'play' && window.history.pushState({}, '', '/')
	
	const handlepopstate = (event: PopStateEvent) => {
		console.log(hostchoice)
		if (hostchoice === 'play') hostchoice = 'choose'
	}
		// TODO: onMount goto /user/login if no user data ?

</script>

<svelte:window on:popstate={handlepopstate} />

{#if ($userdata.username && !$userdata.is_staff) || hostchoice === 'play'}
	<TeamSelect />
{:else}
	<HostChoice bind:hostchoice/>
{/if}