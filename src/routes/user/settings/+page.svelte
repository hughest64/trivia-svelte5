<script lang="ts">
    import { enhance } from '$app/forms';
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';

    const userData = $page.data.user_data;

    const displayMap: Record<string, boolean> = {
        username: false,
        password: false,
        email: false
    };
    const setDisplayed = (key: string) => {
        displayMap[key] = !displayMap[key];
    };
</script>

<svelte:head><title>Trivia Mafa | User Settings</title></svelte:head>

<h1>{userData?.username}</h1>

<h2>Manage your profile</h2>

<button class="button button-primary" class:disabled={displayMap.username} on:click={() => setDisplayed('username')}
    >Update Username</button
>
{#if displayMap.username}
    <form transition:slide action="?/username" method="post" use:enhance>
        <div class="input-container">
            <input type="text" name="username" id="username_id" required />
            <label for="username_id">Username</label>
        </div>
        <button class="button button-tertiary" type="submit">Submit Username</button>
    </form>
{/if}

<button class="button button-primary" on:click={() => setDisplayed('password')}>Update Password</button>
{#if displayMap.password}
    <form transition:slide action="?/password" method="post" use:enhance>
        <div class="input-container">
            <input type="text" name="new_pass" id="new_pass_id" required />
            <label for="new_pass_id">New Password</label>
        </div>
        <button class="button button-tertiary" type="submit">Submit Password</button>
    </form>
{/if}

<button class="button button-primary" on:click={() => setDisplayed('email')}>Update Email</button>
{#if displayMap.email}
    <form transition:slide class="input-container" action="?/email" method="post" use:enhance>
        <div class="input-container">
            <input type="text" name="email" id="email_id" required />
            <label for="email_id">Email</label>
        </div>
        <button class="button button-tertiary" type="submit">Submit Email</button>
    </form>
{/if}

<a href="/" class="button button-tertiary">Go Back</a>

<style lang="scss">
    .disabled {
        color: var(--color-secondary);
        background-color: var(--color-disabled);
    }
    form {
        width: var(--max-element-width);
    }
</style>
