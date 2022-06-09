<script context="module" lang="ts">
    import { browser } from '$app/env';
    import { userdata } from '../../stores/user';
    import type { UserData } from '../../stores/user';
    import * as cookie from 'cookie';
    import type { Load } from '@sveltejs/kit';

    export const load: Load = async({ fetch, session }) => {
        if (browser) return { status: 200 }
        const response = await fetch(
            'http://localhost:8000/user/login/',
            {
                credentials: 'include',
                headers: { accept: 'application/json' }
            }
        )

        if (response.ok) {
            const cookies = response.headers.get('set-cookie')
            const csrftoken = cookies && cookie.parse(cookies)?.csrftoken || ''
            session.csrftoken = csrftoken

        }
        return {
            status: 200,
        }

    }
</script>
<script lang="ts">
    import { goto } from '$app/navigation'
    import { session } from '$app/stores'

    let errorMessage: string;
    let username: string;
    let password: string;

    const validateUser = async() => {
        const response = await fetch(
            'http://localhost:8000/user/login/',
            {
                method: 'POST',
                headers: {
                    'content-type': 'application/json',
                    'Cookie': `csrftoken=${$session.csrftoken}`,
                    'X-CSRFToken': $session.csrftoken,
                },
                body: JSON.stringify({ username, password }),
                credentials: 'include'
            }
        )
        if (response.ok) {
            const data = await <UserData>response.json()
            userdata.set(data)
            // TODO: we need to be able to handle different routing options
            goto('/')

        } else {
            // TODO: we need to handle this better, it's not always bad password or username
            errorMessage = "Bad Username or Password"
        }
    }
</script>

<h1>Login Why Doncha'</h1>

<form on:submit|preventDefault={validateUser}>
    {#if errorMessage}<h3>{errorMessage}</h3>{/if}
    <label for="username">Username:</label>
    <input type="text" id="username" name="username" bind:value={username}>

    <label for="password">Password:</label>
    <input type="password" id="password" name="password" bind:value={password}>

    <input type="submit" value="Log In!">
</form>

<style>
    form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: .75em;
        max-width: 20rem;
        margin: 5rem auto 0;
    }
</style>