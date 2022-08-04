<script context="module" lang="ts">
    import * as cookie from 'cookie';
    import { browser } from '$app/env';
    import { userdata, type UserData } from '$stores/user';
    import { checkStatusCode, getFetchConfig, setCsrfHeaders } from '$lib/utils';
    import type { Load } from '@sveltejs/kit';

    // TODO for migration: this will need to be moved to +page.ts, however...
    // we are currently running this function on the server and setting a cookie header,
    // does that mean we could run this in server.js (i.e, GET for page) and use the 
    // new setHeaders function

    const apiHost = import.meta.env.VITE_API_HOST;

    export const load: Load = async ({ fetch, session }) => {
        if (browser) {
            return { status: 200 };
        }

        const fetchConfig = getFetchConfig('GET');
        const response = await fetch(`${apiHost}/user/login/`, fetchConfig);

        if (response.ok) {
            const cookies = response.headers.get('set-cookie');
            const csrftoken = (cookies && cookie.parse(cookies)?.csrftoken) || '';
            session.csrftoken = csrftoken;
        }

        return checkStatusCode(response);
    };
</script>

<script lang="ts">
    import { goto } from '$app/navigation';
    import { page, session } from '$app/stores';

    $: next = $page.url.searchParams.get('next') || '/';

    export let errorMessage: string;
    let username: string;
    let password: string;

    const validateUser = async () => {
        const fetchConfig = getFetchConfig('POST', { username, password }, setCsrfHeaders($session.csrftoken));
        const response = await fetch(`${apiHost}/user/login/`, fetchConfig);

        if (response.ok) {
            const data: UserData = await response.json();
            userdata.set(data);
            goto(next);

        } else {
            // TODO: we need to handle this better, it's not always bad password or username
            errorMessage = 'Bad Username or Password';
        }
    };
</script>

<svelte:head><title>Trivia Mafia | Login</title></svelte:head>

<h1>Login</h1>

<button class="button button-red">login with Github</button>
<button class="button button-red">login with Google</button>

<h2>-or-</h2>

<form on:submit|preventDefault={validateUser}>
    {#if errorMessage}<h3>{errorMessage}</h3>{/if}
    <div class="input-element">
        <input type="text" id="username" name="username" bind:value={username} />
        <label for="username">Username or Email</label>
    </div>

    <div class="input-element">
        <input type="password" id="password" name="password" bind:value={password} />
        <label for="password">Password</label>
    </div>

    <a href="/user/forgot">Click Here to Reset your Password</a>
    <input class="button button-red" type="submit" value="Submit" />
</form>

<h1>Sign Up</h1>

<button class="button button-white">Create Account</button>

<style>
    h1,
    h2 {
        margin: 0.5em 0;
    }
</style>
