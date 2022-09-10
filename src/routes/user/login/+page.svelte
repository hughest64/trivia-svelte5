<script lang="ts">
    import { page } from '$app/stores';
    // import type { ActionData } from './$types';
    import  type { UserData } from '$stores/user';

    // TODO: this shouldn't be necessary as it should be handled by the ActionData type, I think
    interface FormResponseData {
        error?: string;
        userdata?: UserData;
    }

    export let form: FormResponseData;
    // TODO: the new action api strips the original querystring so we need this sort of gross
    // mechanism in order to hit the correct action and retain the querystring, I consider this a bug
    $: next = `?/login&next=${$page.url.searchParams.get('next') || ''}`;

</script>

<svelte:head><title>Trivia Mafia | Login</title></svelte:head>

<h1>Login</h1>

<button class="button button-red">login with Github</button>
<button class="button button-red">login with Google</button>

<h2>-or-</h2>

<form action={next} method="POST">
    {#if form?.error}<h3>{form?.error}</h3>{/if}
    <div class="input-element">
        <input type="text" id="username" name="username" />
        <label for="username">Username or Email</label>
    </div>

    <div class="input-element">
        <input type="password" id="password" name="password" />
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
