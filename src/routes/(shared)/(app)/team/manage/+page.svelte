<script lang="ts">
    import { page } from '$app/stores';
    import { slide } from 'svelte/transition';
    import { enhance, applyAction } from '$app/forms';
    import { getStore } from '$lib/utils';
    import { getState } from '$lib/state/utils.svelte';
    import type { UserTeam } from '$lib/types';
    import type { Action, ActionResult } from '@sveltejs/kit';

    const qrCode = $page.data.team_qr || '<p>Not Found</p>';

    const prev = $page.url.searchParams.get('prev');

    let userData = getState('userState');
    // $: activeTeam = userData.teams.find((t) => t.id === userData.active_team_id) as UserTeam;

    $: currentName = userData.active_team?.name || '';
    $: nameNotSubmitted = currentName && currentName !== userData.active_team?.name;

    $: currentPassword = userData.active_team?.password || '';
    $: passwordNotSubmitted = currentPassword && currentPassword !== userData.active_team?.password;

    const syncInputText = (e: Event) => {
        const target = <HTMLInputElement>e.target;
        const inputName = target.name;
        if (inputName === 'team_name') {
            currentName = target.value;
        } else if (inputName === 'team_password') {
            currentPassword = target.value;
        }
    };

    let membersDisplayed = false;
    let teamNameDisplayed = false;
    let passwordDisplayed = false;
    let qrCodeDisplayed = false;

    $: form = $page.form;

    const prevRoute = $page.url.searchParams.get('prev') || '/team';

    const handleUpdate = (result: ActionResult, updateType: 'teamName' | 'password') => {
        if (result.type === 'success') {
            const teamToUpdate = userData.teams?.find((t) => t.id === userData.active_team_id);
            if (teamToUpdate && updateType === 'teamName') {
                teamToUpdate.name = currentName;
            } else if (teamToUpdate && updateType === 'password') {
                teamToUpdate.password = currentPassword;
            }
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
                        handleUpdate(result, 'teamName')}
            >
                {#if form?.error?.teamname}<p class="error">{form.error.teamname}</p>{/if}
                {#if form?.success?.teamname}<p>{form?.success?.teamname}</p>{/if}
                <div class="input-container" class:notsubmitted={nameNotSubmitted}>
                    <input
                        type="text"
                        name="team_name"
                        id="team-name"
                        value={userData.active_team.name}
                        on:input={syncInputText}
                        required
                    />
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
                    <input
                        type="text"
                        name="team_password"
                        id="team-password"
                        value={userData.active_team?.password || ''}
                        on:input={syncInputText}
                        required
                    />
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
