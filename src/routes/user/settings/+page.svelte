<script lang="ts">
    import { deserialize, enhance } from '$app/forms';
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';

    $: form = $page.form;
    $: successMsg = form?.success?.msg;
    $: updatedUsername = form?.success?.username;

    const userData = $page.data.user_data;
    let username = userData?.username;

    let autoRevealValue = !!userData?.auto_reveal_questions;

    let formError = '';
    const handleAutoReveal = async (e: Event) => {
        formError = '';
        const target = e.target as HTMLFormElement;

        autoRevealValue = !autoRevealValue;
        const formData = new FormData();
        formData.set('auto_reveal', String(autoRevealValue));

        const response = await fetch(target.action, {
            method: 'post',
            body: formData
        });
        const result = deserialize(await response.text());
        if (result.type === 'failure') {
            formError = result.data?.error as string;
            autoRevealValue = !autoRevealValue;
        }
    };

    const displayMap: Record<string, boolean> = {
        username: false,
        password: false,
        email: false
    };
    const setDisplayed = (key: string) => {
        displayMap[key] = !displayMap[key];
    };

    const updateUsername = () => {
        username = updatedUsername || userData?.username;
        window.scrollTo(0, 0);
    };
    $: successMsg && updateUsername();

    const prevRoute = $page.url.searchParams.get('prev') || '/team';
</script>

<svelte:head><title>Trivia Mafa | User Settings</title></svelte:head>

<h1>{username}</h1>

<h2>Manage your profile</h2>

<form action="?/auto_reveal_update" class="auto-reveal" on:submit|preventDefault={handleAutoReveal}>
    {#if formError} <p class="error">{formError}</p>{/if}
    <div class="switch-container">
        <label for="player_limit" class="switch">
            <input type="checkbox" name="auto_reveal" id="auto-reveal" bind:checked={autoRevealValue} />
            <button id="auto-reveal" type="submit" class="slider round" class:revealed={autoRevealValue} />
        </label>
        <p>Auto Advance</p>
    </div>
    <small>Select this option to auto navigate to the current question when revealed by the host</small>
</form>

{#if successMsg}
    <p>{successMsg}</p>
{/if}
<button class="button button-primary" class:disabled={displayMap.username} on:click={() => setDisplayed('username')}>
    Update Username
</button>
{#if displayMap.username}
    <form transition:slide action="?/user_update" method="post" use:enhance>
        {#if form?.error?.username}<p class="error">{form.error?.username}</p>{/if}
        <div class="input-container">
            <input type="password" name="old_pass" id="old-pass-username" required />
            <label for="old-pass-username">Current Password</label>
        </div>
        <div class="input-container">
            <input type="text" name="username" id="username_id" required />
            <label for="username_id">Username</label>
        </div>
        <button class="button button-tertiary" type="submit">Submit Username</button>
    </form>
{/if}

<button class="button button-primary" on:click={() => setDisplayed('password')}>Update Password</button>

{#if displayMap.password}
    <form transition:slide action="?/user_update" method="post" use:enhance>
        {#if form?.error?.password}<p class="error">{form.error?.password}</p>{/if}
        <div class="input-container">
            <input type="password" name="old_pass" id="old-pass" required />
            <label for="old-pass">Current Password</label>
        </div>
        <div class="input-container">
            <input type="password" name="password" id="new-pass1" required />
            <label for="new-pass1">New Password</label>
        </div>
        <div class="input-container">
            <input type="password" name="password2" id="new-pass2" required />
            <label for="new-pass2">New Password Confirmation</label>
        </div>
        <button class="button button-tertiary" type="submit">Submit Password</button>
    </form>
{/if}

<button class="button button-primary" on:click={() => setDisplayed('email')}>Update Email</button>
{#if displayMap.email}
    <form transition:slide class="input-container" action="?/user_update" method="post" use:enhance>
        {#if form?.error?.email}<p class="error">{form.error?.email}</p>{/if}
        <div class="input-container">
            <input type="password" name="old_pass" id="old-pass-email" required />
            <label for="old-pass-email">Current Password</label>
        </div>
        <div class="input-container">
            <input type="email" name="email" id="email_id" required />
            <label for="email_id">Email</label>
        </div>
        <button class="button button-tertiary" type="submit">Submit Email</button>
    </form>
{/if}

<a href={prevRoute} class="button button-tertiary" data-sveltekit-reload>Go Back</a>

<style lang="scss">
    .switch-container {
        justify-content: space-between;
        margin: 0;
        label {
            margin: 0;
        }
    }
    form {
        width: var(--max-element-width);
        max-width: calc(100% - 0.25rem);
    }
</style>
