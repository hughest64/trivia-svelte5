<script lang="ts">
    import { env } from '$env/dynamic/public';
    import { page } from '$app/stores';

    $: form = $page.form;
    $: loaderror = $page.data.loaderror;

    const googleAuthParams = new URLSearchParams({
        client_id: env.PUBLIC_GOOGLE_CLIENT_ID,
        // TODO: get from env variable or use url.host?
        redirect_uri: 'http://127.0.0.1:5173/user/google-auth',
        scope: [
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'
        ].join(' '),
        response_type: 'code',
        access_type: 'offline',
        prompt: 'consent'
    });
    $: googleUrl = `https://accounts.google.com/o/oauth2/v2/auth?${googleAuthParams}`;
</script>

<svelte:head><title>Trivia Mafia | Login</title></svelte:head>

<h1>Login</h1>

{#if loaderror}
    <h3>{loaderror}</h3>
{:else}
    <button class="button button-primary">login with Github</button>
    <a href={googleUrl} class="button button-primary">login with Google</a>

    <h2>-or-</h2>

    <!-- TODO: add an action, maybe action='?/login' -->
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
