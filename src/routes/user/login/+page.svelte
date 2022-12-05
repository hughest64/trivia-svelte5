<script lang="ts">
    import type { ActionData } from './$types';

    export let form: ActionData;
</script>

<svelte:head><title>Trivia Mafia | Login</title></svelte:head>

<h1>Login</h1>

<button class="button button-red">login with Github</button>
<button class="button button-red">login with Google</button>

<h2>-or-</h2>

<form method="POST">
    {#if form?.error}<h3>{form?.error}</h3>{/if}
    <div class="input-element">
        <input type="text" id="username" name="username" autocapitalize="off" autocomplete="username" />
        <label for="username">Username or Email</label>
    </div>

    <div class="input-element">
        <input type="password" id="password" name="password" autocomplete="current-password" />
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
