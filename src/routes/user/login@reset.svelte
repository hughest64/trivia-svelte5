<!-- <script context="module" lang="ts">
    import { browser } from '$app/env';
    import * as cookie from 'cookie';

    // @ts-ignore
    export async function load({ fetch }) {
        if (!browser) return { status: 200 }
        const response = await fetch(
            'http://localhost:8000/user/login/',
            { credentials: 'include' }
        )

        let csrftoken: string;
        if (response.ok) {
            try {
                csrftoken = cookie.parse(
                    <string>response.headers.get('set-cookie')
                )?.csrftoken || ''
            } catch {}

        }
        return {
            status: 200,
            props: {
                csrftoken
            }
        }

    }
</script> -->
<script lang="ts">
    import { goto } from '$app/navigation'

    let errorMessage: string;
    let username: string;
    let password: string;
    // export let csrftoken: string;
    // $: console.log(csrftoken)

    const validateUser = async() => {
        const response = await fetch(
            'http://localhost:8000/user/login/',
            {
                method: 'POST',
                headers: {'content-type': 'application/json'},
                body: JSON.stringify({ username, password }),
                credentials: 'include'
            }
        )
        if (response.ok) {
            goto('/')
        } else {
            errorMessage = "Bad Username or Password"
        }
        console.log(response)
    }
</script>

<h1>Login Why Doncha'</h1>

<form on:submit|preventDefault={validateUser}>
<!-- <form action="/user/login" method="post" name="login"> -->
    {#if errorMessage}<h3>{errorMessage}</h3>{/if}
    <!-- <input type="hidden" id="csrftoken" name="csrftoken" value={csrftoken}> -->
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