<script lang="ts">
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    // import type { ActionData } from './$types';
    import { userdata, type UserData } from '$stores/user';
    import { browser } from '$app/environment';

    // TODO: this shouldn't be necessary as it should be handled by the ActionData type, I think
    interface FormResponseData {
        error?: string;
        userdata?: UserData;
    }

    export let form: FormResponseData;
    // we can't use goto browser side
    $: if (form?.userdata && browser) {
        userdata.set(form.userdata);
        const next = $page.url.searchParams.get('next') || $userdata.is_staff ? '/host/choice' : '/team';

        goto(next);
    }
</script>

<svelte:head><title>Trivia Mafia | Login</title></svelte:head>

<h1>Login</h1>

<button class="button button-red">login with Github</button>
<button class="button button-red">login with Google</button>

<h2>-or-</h2>

<form action="?/login" method="POST">
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
