<script context="module" lang="ts">
	import * as cookie from 'cookie';
	import { browser } from '$app/env';
	import { userdata, type UserData } from '$stores/user';
	import { checkStatusCode, getFetchConfig, setCsrfHeaders } from '$lib/utils';
	import type { Load } from '@sveltejs/kit';
	const apiHost = import.meta.env.VITE_API_HOST;

	export const load: Load = async ({ fetch, session }) => {
		if (browser) return { status: 200 }; // TODO: do we still need the broswer check?
		
        const fetchConfig = getFetchConfig('GET');
		const response = await fetch(`${apiHost}/user/login/`, fetchConfig);

		if (response.ok) {
			const cookies = response.headers.get('set-cookie');
			const csrftoken = (cookies && cookie.parse(cookies)?.csrftoken) || '';
			session.csrftoken = csrftoken;
		}

		return checkStatusCode(response)
	};
</script>

<script lang="ts">
	import { goto } from '$app/navigation';
	import { page, session } from '$app/stores';

    $: next = $page.url.searchParams.get('next') || '/'

	let errorMessage: string;
	let username: string;
	let password: string;

	const validateUser = async () => {
		const fetchConfig = getFetchConfig(
            'POST',
            { username, password },
            setCsrfHeaders($session.csrftoken)
        );

		const response = await fetch(`${apiHost}/user/login/`, fetchConfig);

		if (response.ok) {
			const data: UserData = await response.json();
			userdata.set(data);
			// TODO: revert back to goto once the login view returns team data
            // for now we need to do this so that the module script at / will run
			window.open(next, '_self');
			// goto(next)
		} else {
			// TODO: we need to handle this better, it's not always bad password or username
			errorMessage = 'Bad Username or Password';
		}
	};
</script>

<h1>Welcome!</h1>

<form on:submit|preventDefault={validateUser}>
	{#if errorMessage}<h3>{errorMessage}</h3>{/if}
	<label for="username">Username:</label>
	<input type="text" id="username" name="username" bind:value={username} />

	<label for="password">Password:</label>
	<input type="password" id="password" name="password" bind:value={password} />

	<input type="submit" value="Log In!" />
</form>

<style>
	form {
		display: flex;
		flex-direction: column;
		justify-content: center;
		gap: 0.75em;
		max-width: 20rem;
		margin: 5rem auto 0;
	}
</style>
