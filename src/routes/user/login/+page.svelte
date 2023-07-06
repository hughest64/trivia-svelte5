<script lang="ts">
    import { page } from '$app/stores';
    import { googleAuthUrl, githubAuthUrl } from '../utils';
    import * as cookie from 'cookie';

    $: form = $page.form;
    $: loaderror = $page.data.loaderror;

    const setNextEndPoint = () => {
        const nextParam = $page.url.searchParams.get('next');
        if (!nextParam) return;

        const nextCookie = cookie.serialize('next', nextParam, { path: '/', httpOnly: false, sameSite: true });
        document.cookie = nextCookie;
    };
</script>

<svelte:head><title>Trivia Mafia | Login</title></svelte:head>

<h1>Login</h1>

{#if loaderror}
    <h3>{loaderror}</h3>
{:else}
    <a href={githubAuthUrl()} class="button button-primary" on:click={setNextEndPoint}>login with Github</a>
    <a href={googleAuthUrl()} class="button button-primary" on:click={setNextEndPoint}>login with Google</a>

    <h2>-or-</h2>

    <form action="" method="POST">
        {#if form?.error}<h3>{form?.error}</h3>{/if}
        <div class="input-container">
            <input type="text" id="username" name="username" autocapitalize="off" autocomplete="username" required />
            <label for="username">Username or Email</label>
        </div>

        <div class="input-container">
            <input type="password" id="password" name="password" autocomplete="current-password" required />
            <label for="password">Password</label>
        </div>

        <a href="/user/forgot">Click Here to Reset your Password</a>
        <button type="submit" class="button button-primary">Submit</button>
    </form>

    <h1>Sign Up</h1>

    <a class="button button-tertiary signup-link" href="/user/create">Create Account</a>
{/if}

<style lang="scss">
    .signup-link {
        text-decoration: none;
        color: var(--color-secondary);
    }
</style>
