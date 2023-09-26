<script lang="ts">
    import { page } from '$app/stores';
    import { slide } from 'svelte/transition';
    import { deserialize } from '$app/forms';
    import { getStore } from '$lib/utils';
    import type { UserData } from '$lib/types';

    const joincode = $page.url.searchParams.get('joincode') || '0';

    const userData = getStore('userData');
    $: activeTeam = $userData.teams.find((t) => t.id === $userData.active_team_id);
    $: currentName = activeTeam?.name || '';
    $: notsubmitted = currentName && currentName !== activeTeam?.name;

    const syncInputText = (e: Event) => {
        const target = <HTMLInputElement>e.target;
        currentName = target.value;
    };

    let membersDisplayed = false;
    let teamNameDisplayed = true;

    let formError = '';
    let successMsg = '';
    const handleTeamNameUpdate = async (e: Event) => {
        if (!notsubmitted) return;
        formError = '';
        successMsg = '';

        const target = e.target as HTMLFormElement;
        const data = new FormData();
        data.append('team_name', currentName);
        data.append('team_id', String(activeTeam?.id));

        const response = await fetch(target.action, {
            method: 'post',
            body: data
        });
        const result = deserialize(await response.text());
        if (result.type === 'failure') {
            formError = result.data?.error as string;
            (document.getElementById('team-name') as HTMLInputElement).value = activeTeam?.name!;
            notsubmitted = false;
        }
        if (result.type === 'success') {
            successMsg = 'Your team name has been updated!';
            $userData = result.data!.user_data as UserData;
        }
    };
</script>

<svelte:head><title>Trivia Mafia | Manage Team</title></svelte:head>

<main class="short">
    {#if activeTeam}
        <h1>{activeTeam?.name}</h1>
        <h3>Manage Your Team</h3>

        <button
            class="button button-primary"
            class:disabled={membersDisplayed}
            on:click={() => (membersDisplayed = !membersDisplayed)}
        >
            Team Members
        </button>

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
                on:submit|preventDefault={handleTeamNameUpdate}
            >
                {#if formError}<p class="error">{formError}</p>{/if}
                {#if successMsg}<p>{successMsg}</p>{/if}
                <div class="input-container" class:notsubmitted>
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
    {:else}
        <!-- TODO: link to team select or create -->
        <h1>You don't have a team selected</h1>
    {/if}
</main>

<style lang="scss">
    .notsubmitted {
        input {
            border-color: var(--color-primary);
        }
        label {
            background-color: var(--color-primary);
        }
    }
</style>
