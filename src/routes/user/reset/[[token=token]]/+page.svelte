<script lang="ts">
    import { enhance } from '$app/forms';
    export let form: Record<string, unknown>;
</script>

<svelte:head><title>Trivia Mafia | Reset Password</title></svelte:head>

<h1>Password Reset</h1>

<form action="" method="post" use:enhance>
    {#if form?.error}
        <p class="error">{form.error}</p>
    {/if}
    <div class="input-container">
        <input type="password" name="pass1" id="pass1" required />
        <label for="pass1">Password</label>
    </div>

    <div class="input-container">
        <input type="password" name="pass2" id="pass2" required />
        <label for="pass2">Password Confirmation</label>
    </div>

    <button type="submit" class="button button-primary">Update Password</button>
</form>
