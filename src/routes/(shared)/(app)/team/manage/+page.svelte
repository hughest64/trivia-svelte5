<script lang="ts">
    import { page } from '$app/stores';
    import { slide } from 'svelte/transition';
    import { enhance, applyAction } from '$app/forms';
    import { getState } from '$lib/state/utils.svelte';
    import type { ActionResult } from '@sveltejs/kit';

    // TODO: s5 - data should probably come from $props()
    const qrCode = $page.data.team_qr || '<p>Not Found</p>';
    const prev = $page.url.searchParams.get('prev');

    // TDOO: s5 figure out typing here
    let { form }: Record<string, any> = $props();

    let userData = getState('userState');

    // bind form values that will be synced upon successful form submission
    let visibleTeamName = $state(userData.active_team?.name || '');
    let visiblePassword = $state(userData.active_team?.password || '');

    // apply a red border to inputs when the value doesn't match the state value
    let nameNotSubmitted = $derived(visibleTeamName && visibleTeamName !== userData.active_team?.name);
    let passwordNotSubmitted = $derived(visiblePassword && visiblePassword !== userData.active_team?.password);

    // controls for which form is visible
    let membersDisplayed = $state(false);
    let teamNameDisplayed = $state(true);
    let passwordDisplayed = $state(false);
    let qrCodeDisplayed = $state(false);

    const prevRoute = $page.url.searchParams.get('prev') || '/team';

    const handleUpdate = (result: ActionResult, updateType: 'name' | 'password') => {
        if (result.type == 'success') {
            console.log(updateType, 'updating');
            userData.updateActiveTeamData(updateType, updateType === 'name' ? visibleTeamName : visiblePassword);
        }
        applyAction(result);
    };
</script>

<svelte:head><title>Trivia Mafia | Manage Team</title></svelte:head>

<main class="short">
    {#if userData.active_team}
        <h1 class="name-header">{userData.active_team.name}</h1>

        <p>Password: {userData.active_team.password}</p>

        <h3>Manage Your Team</h3>

        <button
            class="button button-primary"
            class:disabled={qrCodeDisplayed}
            on:click={() => (qrCodeDisplayed = !qrCodeDisplayed)}
        >
            {qrCodeDisplayed ? 'Hide' : 'Show'} QR Code
        </button>

        {#if qrCodeDisplayed}
            <div transition:slide>
                {@html qrCode}
            </div>
        {/if}

        <button
            class="button button-primary"
            class:disabled={membersDisplayed}
            on:click={() => (membersDisplayed = !membersDisplayed)}
        >
            Team Members
        </button>

        {#if membersDisplayed && userData.active_team?.members?.length}
            <form
                transition:slide
                action="?/remove-team-members&team_id={userData.active_team_id}"
                method="post"
                use:enhance
            >
                {#if form?.error}<p class="error">{form.error}</p>{/if}
                <ul class="member-container">
                    <li class="member">
                        <strong>Member Name</strong>
                        <strong>Remove</strong>
                    </li>
                    {#each userData.active_team.members as member}
                        {#if member !== userData.username}
                            <li class="member">
                                <label for="team-member-{member}">{member}</label>
                                <input type="checkbox" name={member} id="team-member-{member}" />
                            </li>
                            <!-- {:else}
                            <li class="member">
                                <div>{member}</div>
                                <div>It's You!</div>
                            </li> -->
                        {/if}
                    {/each}
                </ul>
                <button class="button button-tertiary">Remove Team Members</button>
            </form>
        {/if}

        <button
            class="button button-primary"
            class:disabled={teamNameDisplayed}
            on:click={() => (teamNameDisplayed = !teamNameDisplayed)}
        >
            Update Team Name
        </button>

        {#if teamNameDisplayed}
            <form
                transition:slide
                action="?/updatename&prev={prev}"
                method="post"
                use:enhance={() =>
                    ({ result }) =>
                        handleUpdate(result, 'name')}
            >
                {#if form?.error?.teamname}<p class="error">{form.error.teamname}</p>{/if}
                {#if form?.success?.teamname}<p>{form?.success?.teamname}</p>{/if}
                <div class="input-container" class:notsubmitted={nameNotSubmitted}>
                    <input type="text" name="team_name" id="team-name" bind:value={visibleTeamName} required />
                    <label for="team-name">Team Name</label>
                </div>
                <button class="button button-tertiary">Update</button>
            </form>
        {/if}

        <button class="button button-primary" on:click={() => (passwordDisplayed = !passwordDisplayed)}>
            Update Team Password
        </button>
        {#if passwordDisplayed}
            <form
                transition:slide
                action="?/update-password&prev={prev}"
                method="post"
                use:enhance={() =>
                    ({ result }) =>
                        handleUpdate(result, 'password')}
            >
                {#if form?.error?.password}<p class="error">{form.error.password}</p>{/if}
                {#if form?.success?.password}<p>{form.success.password}</p>{/if}
                <div class="input-container" class:notsubmitted={passwordNotSubmitted}>
                    <input type="text" name="team_password" id="team-password" bind:value={visiblePassword} required />
                    <label for="team-password">Team Password</label>
                </div>
                <button class="button button-tertiary">Update</button>
            </form>
        {/if}
    {:else}
        <!-- TODO: link to team select or create -->
        <h1>You don't have a team selected</h1>
    {/if}
    <a href={prevRoute} class="button button-tertiary" data-sveltekit-reload>Go Back</a>
</main>

<style lang="scss">
    .name-header {
        margin-bottom: 0;
    }
    .member-container {
        width: var(--max-element-width);
        max-width: calc(100vw - 2rem);
    }
    .member {
        display: flex;
        justify-content: space-between;
        font-size: 1.25rem;
        padding: 0.5rem 0;
    }
    .notsubmitted {
        input {
            border-color: var(--color-primary);
        }
        label {
            background-color: var(--color-primary);
        }
    }
</style>
