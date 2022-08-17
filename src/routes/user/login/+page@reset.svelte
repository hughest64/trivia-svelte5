<script lang="ts">
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { getFetchConfig, setCsrfHeaders } from '$lib/utils';
    import { userdata } from '$stores/user';
    import type { UserData } from '$stores/user';
    import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

    $: csrftoken = $page.data?.csrftoken || 'not-set';

    $: next = $page.url.searchParams.get('next') || '/';

    export let errorMessage: string;
    let username: string;
    let password: string;

    const validateUser = async () => {
        const fetchConfig = getFetchConfig('POST', { username, password }, setCsrfHeaders(csrftoken));
        console.log(fetchConfig);
        // const response = await fetch(`${apiHost}/user/login/`, fetchConfig);

        // if (response.ok) {
        //     const data: UserData = await response.json();
        //     userdata.set(data);
        //     goto(next);
        // } else {
        //     // TODO: we need to handle this better, it's not always bad password or username
        //     errorMessage = 'Bad Username or Password';
        // }
    };
</script>

<svelte:head><title>Trivia Mafia | Login</title></svelte:head>

<h1>Login</h1>

<button class="button button-red">login with Github</button>
<button class="button button-red">login with Google</button>

<h2>-or-</h2>

<!-- <form on:submit|preventDefault={validateUser}> -->
<form action='' method="POST">
    {#if errorMessage}<h3>{errorMessage}</h3>{/if}
    <input hidden name="csrftoken" value={csrftoken}>
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
