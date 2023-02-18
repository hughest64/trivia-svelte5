<script lang="ts">
    import { enhance } from '$app/forms';
    import type { ActionData } from './$types';

    export let form: ActionData;
</script>

<h1>Sign Up</h1>

<form action="" method="post" use:enhance>
    {#if form?.error}<p>{form.error}</p>{/if}
    <!-- {#if form?.success}<p>Your user was created!</p>{/if} -->
    <div class="input-container">
        <input type="text" name="username" id="username" required />
        <label for="username">Username</label>
    </div>
    <div class="input-container">
        <input type="password" name="pass" id="pass" required />
        <label for="">Password</label>
    </div>
    <div class="input-container">
        <input type="password" name="pass2" id="pass2" required />
        <label for="pass2">Password Confirmation</label>
    </div>
    <div class="input-container">
        <input type="email" name="email" id="email" required />
        <label for="email">Email Address</label>
    </div>
    <button type="submit" class="button button-primary">Sign Up</button>
</form>
