<script lang="ts">
    import { page } from '$app/stores';
    import { enhance } from '$app/forms';

    $: form = $page.form;
    $: loaderror = $page.data.loaderror;

    const teamPassword = $page.url.searchParams.get('password') || '';
    const next = $page.url.searchParams.get('next') || '';
</script>

<svelte:head><title>Trivia Mafia | Login</title></svelte:head>

<h1>Login</h1>

{#if loaderror}
    <h3>{loaderror}</h3>
{:else}
    <form action="/user/google-auth?/auth" method="post" class="form" use:enhance>
        <input type="hidden" name="team_password" id="team-password" value={teamPassword} />
        <input type="hidden" name="next" id="next-route" value={next} />
        <button class="button button-primary" type="submit">login with Google</button>
    </form>

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

    <a class="button button-tertiary signup-link" href="/user/create{$page.url.search}">Create Account</a>
{/if}

<style lang="scss">
    .signup-link {
        text-decoration: none;
        color: var(--color-secondary);
    }
</style>
