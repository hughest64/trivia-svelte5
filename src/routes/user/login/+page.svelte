<script lang="ts">
    import type { ActionData } from './$types';

    export let form: ActionData;
</script>

<svelte:head><title>Trivia Mafia | Login</title></svelte:head>

<h1>Login</h1>

<button class="button button-primary">login with Github</button>
<button class="button button-primary">login with Google</button>

<h2>-or-</h2>

<!-- TODO: add an action, maybe action='?/login' -->
<form method="POST">
    {#if form?.error}<h3>{form?.error}</h3>{/if}
    <div class="input-container">
        <input type="text" id="username" name="username" autocapitalize="off" autocomplete="username" required />
        <label for="username">Username or Email</label>
    </div>

    <div class="input-container">
        <input type="password" id="password" name="password" autocomplete="current-password" required />
        <label for="password">Password</label>
    </div>

    <!-- not yet implemented, but the input will likely need to be a button with a formAction -->
    <a href="/user/forgot">Click Here to Reset your Password</a>
    <!-- <input class="button button-primary" type="submit" value="Submit" /> -->
    <button type="submit" class="button button-primary">Submit</button>
</form>

<h1>Sign Up</h1>

<a class="button button-tertiary signup-link" href="/user/create">Create Account</a>

<style lang="scss">
    .signup-link {
        text-decoration: none;
        color: var(--color-secondary);
    }
</style>
