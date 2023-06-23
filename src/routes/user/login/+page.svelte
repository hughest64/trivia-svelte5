<script lang="ts">
    import { page } from '$app/stores';

    $: form = $page.form;
    $: loaderror = $page.data.loaderror;
</script>

<svelte:head><title>Trivia Mafia | Login</title></svelte:head>

<h1>Login</h1>

{#if loaderror}
    <h3>{loaderror}</h3>
{:else}
    <button class="button button-primary">login with Github</button>
    <button class="button button-primary">login with Google</button>

    <h2>-or-</h2>

    <!-- TODO: add an action, maybe action='?/login' -->
    <form action="?/login" method="POST">
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
