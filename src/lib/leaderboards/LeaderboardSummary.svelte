<script lang="ts">
    import { page } from '$app/stores';
    import { applyAction, enhance } from '$app/forms';
    import { getStore, respsByround, splitQuestionKey } from '$lib/utils';
    import RoundResponses from '$lib/leaderboards/RoundResponses.svelte';
    import EditTeamName from './icons/EditTeamName.svelte';
    import PointsAdjustment from './PointsAdjustment.svelte';
    import type { LeaderboardEntry, ResponseMeta } from '$lib/types';

    export let entry: LeaderboardEntry | undefined;
    $: teamName = entry?.team_name;

    $: isHost = $page.url.pathname.startsWith('/host');

    const rounds = getStore('rounds');
    const roundStates = getStore('roundStates');
    const teamResponseStore = getStore('responseData');
    $: groupedResps = respsByround($teamResponseStore, $rounds, $roundStates, false);

    let nameEditable = false;
    const syncInputText = (e: Event) => {
        const target = <HTMLInputElement>e.target;
        teamName = target.value;
    };

    $: isMegaRound = (group: ResponseMeta[]) => splitQuestionKey(group[0].key).round === String(entry?.megaround);
</script>

{#if entry}
    <form
        action="/host/{$page.params.joincode}/leaderboard?/updateteamname"
        method="post"
        class="name-form"
        use:enhance={() =>
            ({ result }) => {
                nameEditable = false;
                applyAction(result);
            }}
    >
        {#if nameEditable}
            <input type="hidden" name="team_id" value={entry.team_id} />
            <input type="text" class="team-name" name="team_name" value={teamName} on:input={syncInputText} />
            <button class="submit-btn" type="submit">✓</button>
        {:else}
            <h2><strong>{entry.team_name}</strong></h2>
            <button on:click={() => (nameEditable = !nameEditable)}>
                <EditTeamName />
            </button>
        {/if}
    </form>

    <div class="answer-container">
        <p class="team-password">Team Password: {entry.team_password}</p>
        <div class="leaderboard-meta">
            <p><strong>Place:</strong> {entry.rank}</p>
            <p><strong>Points:</strong> {entry.total_points}</p>
        </div>
        <ul class="response-round-list">
            {#each groupedResps || [] as group}
                <li class:megaround={isMegaRound(group)}>
                    {#if isMegaRound(group)}
                        <h3>Mega Round!</h3>
                    {/if}
                    <RoundResponses roundResps={group} />
                </li>
            {/each}
        </ul>
    </div>
    {#if isHost}
        <PointsAdjustment bind:entry />
    {/if}
{:else}
    <h2 class="error">A summary is not currently available</h2>
{/if}

<style lang="scss">
    .leaderboard-meta {
        display: flex;
        justify-content: space-between;
    }
    .name-form {
        flex-direction: row;
        justify-content: center;
        gap: 1rem;
    }
    .team-name {
        font-size: 1.25rem;
        font-weight: bold;
        font-family: 'Montserrat';
        padding: 0.3rem;
        border: 2px solid var(--color-secondary);
        border-radius: 5px;
    }
    .submit-btn {
        font-size: 24px;
        font-weight: bold;
        width: 2.5rem;
        height: 2.5rem;
        background-color: var(--color-current);
        border: 2px solid var(--color-secondary);
        border-radius: 5px;
    }
    .megaround {
        border: 2px solid var(--color-primary);
        border-radius: 10px;
        h3 {
            padding: 0.5rem;
            padding-bottom: 0;
        }
    }
</style>
