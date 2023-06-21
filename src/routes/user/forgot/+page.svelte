<script lang="ts">
    import { enhance } from '$app/forms';
    export let form: Record<string, unknown>;
</script>

<h1>Password Reset</h1>

<form action="" method="POST" use:enhance>
    {#if form?.info}
        <p class="error">{form.info}</p>
    {/if}
    <div class="input-container">
        <input type="text" name="username" id="username" required />
        <label for="username">Username or Email</label>
    </div>
    <button class="button button-primary">Request a Password Reset</button>
</form>
