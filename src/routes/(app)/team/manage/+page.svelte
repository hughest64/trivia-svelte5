<script lang="ts">
    import { page } from '$app/stores';
    import { browser } from '$app/environment';
    import { afterNavigate, beforeNavigate } from '$app/navigation';
    import { slide } from 'svelte/transition';
    import { deserialize, enhance, applyAction } from '$app/forms';
    import { getStore } from '$lib/utils';
    import type { UserTeam } from '$lib/types';

    const joincode = $page.url.searchParams.get('joincode') || '0';

    const userData = getStore('userData');
    $: activeTeam = $userData.teams.find((t) => t.id === $userData.active_team_id) as UserTeam;

    $: currentName = activeTeam?.name || '';
    $: nameNotSubmitted = currentName && currentName !== activeTeam?.name;

    $: currentPassword = activeTeam?.password || '';
    $: passwordNotSubmitted = currentPassword && currentPassword !== activeTeam?.password;

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

    $: form = $page.form;

    const clearStorage = () => sessionStorage.removeItem('previous_route');
    let prevRoute = (browser && sessionStorage.getItem('previous_route')) || '/team';
    afterNavigate(({ from, to }) => {
        const fromPath = from?.url.pathname as string;
        const toPath = to?.url.pathname as string;
        if (fromPath && fromPath !== toPath) {
            prevRoute = fromPath;
            sessionStorage.setItem('previous_route', fromPath);
        }
    });

    // hijack navigation in case of the back button being pressed which does weird things
    beforeNavigate(({ to }) => {
        clearStorage();
        if (to?.url) window.location.assign(to.url);
    });
</script>

<svelte:head><title>Trivia Mafia | Manage Team</title></svelte:head>

<main class="short">
    {#if activeTeam}
        <h1>{activeTeam.name}</h1>
        <h3>Manage Your Team</h3>

        <button
            class="button button-primary"
            class:disabled={membersDisplayed}
            on:click={() => (membersDisplayed = !membersDisplayed)}
        >
            Team Members
        </button>

        {#if membersDisplayed && activeTeam?.members?.length}
            <form
                transition:slide
                action="?/remove-team-members&team_id={$userData.active_team_id}"
                method="post"
                use:enhance
            >
                {#if form?.error}<p class="error">{form.error}</p>{/if}
                <ul class="member-container">
                    <li class="member">
                        <strong>Member Name</strong>
                        <strong>Remove</strong>
                    </li>
                    {#each activeTeam.members as member}
                        {#if member !== $userData.username}
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
                action="?/updatename&joincode={joincode}"
                method="post"
                use:enhance={() =>
                    ({ result }) => {
                        if (result.type === 'success') {
                            userData.update((u) => {
                                const newData = { ...u };
                                const teamToUpdate = u.teams?.find((t) => t.id === $userData.active_team_id);
                                if (teamToUpdate) teamToUpdate.name = currentName;
                                return newData;
                            });
                        }
                        applyAction(result);
                    }}
            >
                {#if form?.error?.teamname}<p class="error">{form.error.teamname}</p>{/if}
                {#if form?.success?.teamname}<p>{form?.success?.teamname}</p>{/if}
                <div class="input-container" class:notsubmitted={nameNotSubmitted}>
                    <input
                        type="text"
                        name="team_name"
                        id="team-name"
                        value={activeTeam.name}
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
                action="?/update-password&joincode={joincode}"
                method="post"
                use:enhance={() =>
                    ({ result }) => {
                        applyAction(result);
                    }}
            >
                {#if form?.error?.password}<p class="error">{form.error.password}</p>{/if}
                {#if form?.success?.password}<p>{form.success.password}</p>{/if}
                <div class="input-container" class:notsubmitted={passwordNotSubmitted}>
                    <input
                        type="text"
                        name="team_password"
                        id="team-password"
                        value={activeTeam?.password || ''}
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
    <a href={prevRoute} class="button button-tertiary" on:click={clearStorage}>Go Back</a>
</main>

<style lang="scss">
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
