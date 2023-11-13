<script lang="ts">
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import { applyAction, enhance } from '$app/forms';
    import { getStore, respsByround, splitQuestionKey } from '$lib/utils';
    import EditTeamName from './icons/EditTeamName.svelte';
    import RoundResponses from './RoundResponses.svelte';
    import PointsAdjustment from './PointsAdjustment.svelte';
    import type { LeaderboardEntry } from '$lib/types';

    export let entry: LeaderboardEntry;
    export let lbView: 'public' | 'host' = 'public';

    $: teamName = entry.team_name;

    const userStore = getStore('userData');
    const isPlayerEndpoint = $page.url.pathname.startsWith('/game');

    $: isPlayerTeamEntry = entry.team_id === $userStore.active_team_id;
    $: expandable = (!isPlayerEndpoint && lbView === 'host') || (isPlayerEndpoint && isPlayerTeamEntry);

    const rounds = getStore('rounds');
    const roundStates = getStore('roundStates');
    $: isSecondHalf = Math.max(...$roundStates.map((rs) => (rs.scored ? rs.round_number : 0)));

    const teamResponseStore = getStore('responseData');
    $: responses = (expandable && $teamResponseStore) || [];
    $: isHost = $page.url.pathname.startsWith('/host');
    $: groupedResps = respsByround(responses, $rounds, $roundStates, isHost);

    let expanded = false;
    $: collapsed = !expandable ? null : !expanded;

    let fetched = false;
    let nameEditable = false;
    const handleExpand = async () => {
        if (!expandable) return;

        if (expanded) {
            teamName = entry.team_name;
            nameEditable = false;
        }

        if (isPlayerEndpoint || fetched) {
            expanded = !expanded;
            return;
        }

        const resp = await fetch(`${$page.url.pathname}/responses/${entry.team_id}`);
        if (resp.ok) {
            responses = (await resp.json())?.responses || [];
            fetched = true;
        } else {
            // TODO: handle error state
        }

        expanded = !expanded;
    };

    const syncInputText = (e: Event) => {
        const target = <HTMLInputElement>e.target;
        teamName = target.value;
    };
</script>

<li class="leaderboard-entry-container">
    <div class="leaderboard-entry-meta">
        <button class="rank" class:collapsed class:expanded on:click={handleExpand}>
            <h3 class="rank-display">{entry.rank}</h3>
        </button>

        <div class="team-name grow" class:team-name-wide={collapsed}>
            {#if !expanded}
                <button class="team-name-btn" on:click={handleExpand}>
                    <h3 class="team-name-display">{teamName}</h3>
                    {#if (isPlayerTeamEntry || !isPlayerEndpoint) && isSecondHalf && !entry.megaround}
                        <span class="megaround-alert">!Mega Round</span>
                    {/if}
                </button>
            {:else}
                <form
                    action="/host/{$page.params.joincode}/leaderboard?/updateteamname"
                    method="post"
                    use:enhance={() =>
                        ({ result }) => {
                            nameEditable = false;
                            applyAction(result);
                        }}
                >
                    {#if nameEditable}
                        <input type="hidden" name="team_id" value={entry.team_id} />
                        <input type="text" name="team_name" value={teamName} on:input={syncInputText} />
                        <button class="edit-teamname submit-btn" type="submit">✓</button>
                    {:else if expanded}
                        <button on:click={handleExpand}><h3>{teamName}</h3></button>
                        <button class="edit-teamname" on:click={() => (nameEditable = !nameEditable)}>
                            <EditTeamName />
                        </button>
                        <button class="grow filler-btn" on:click={handleExpand}>-</button>
                    {/if}
                </form>
            {/if}
        </div>

        <button class="points" on:click={handleExpand}>
            <h3 class="points-display">{entry.total_points}</h3>
        </button>
    </div>

    {#if expanded}
        <div transition:slide class="answer-container">
            <p class="team-password">Team Password: {entry.team_password}</p>
            <ul class="response-round-list">
                {#each groupedResps || [] as group}
                    {@const isMegaRound =
                        expandable && splitQuestionKey(group[0].key).round === String(entry.megaround)}
                    <li class:megaround={isMegaRound}>
                        {#if isMegaRound}
                            <h3>Mega Round!</h3>
                        {/if}
                        <RoundResponses roundResps={group} />
                    </li>
                {/each}
            </ul>
        </div>
    {/if}
    {#if !isPlayerEndpoint && expanded}
        <PointsAdjustment {entry} />
    {/if}
</li>

<style lang="scss">
    .leaderboard-entry-container {
        width: 100%;
        margin: 0.5rem 0;
        border: 2px solid var(--color-secondary);
        border-radius: 10px;
        & > * {
            display: flex;
            align-items: center;
        }
        .leaderboard-entry-meta {
            display: flex;
            width: 100%;
            padding: 0;
            margin: 0;
        }
        .rank {
            justify-content: center;
            min-width: 3.5rem;
            padding: 1.25rem;
            background-color: var(--color-alt-black);
            color: var(--color-tertiary);
        }
        .expanded {
            border-bottom-right-radius: 10px;
            position: relative;
            ::after {
                content: '';
                position: absolute;
                bottom: -0.6rem;
                background-repeat: no-repeat;
                background-image: url("data:image/svg+xml;utf8,%3Csvg%20viewBox%3D'0%200%2033.073%2033.073'%20xmlns%3D'http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg'%3E%3Cpath%20d%3D'M.057%2014.357l16.48%2011.54%2016.479-11.54z'%20fill%3D'%23eb5757'%2F%3E%3C%2Fsvg%3E");
                width: 70%;
                height: 70%;
                left: 15%;
            }
        }
        .collapsed {
            position: relative;
            ::after {
                content: '';
                position: absolute;
                bottom: -1rem;
                background-repeat: no-repeat;
                background-image: url("data:image/svg+xml;utf8,%3Csvg%20viewBox%3D'0%200%2033.073%2033.073'%20transform%3D'scale(-1%20-1)'%20xmlns%3D'http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg'%3E%3Cpath%20d%3D'M.057%2014.357l16.48%2011.54%2016.479-11.54z'%20fill%3D'%23eb5757'%2F%3E%3C%2Fsvg%3E");
                width: 70%;
                height: 70%;
                left: 15%;
            }
        }
        .team-name {
            margin: 0.5rem 0;
            padding: 0 1rem;
            form {
                display: flex;
                flex-direction: row;

                gap: 1rem;
            }
            input {
                font-size: 1.25rem;
                font-weight: bold;
                font-family: 'Montserrat';
                padding: 0.3rem;
                border: 2px solid var(--color-secondary);
                border-radius: 5px;
            }
            button {
                position: relative;
                text-align: left;
            }
            .team-name-btn {
                width: 100%;
            }
        }
        .edit-teamname {
            margin: 0;
            padding: 0;
            flex-grow: 1;
            text-align: left;
        }
        .submit-btn {
            flex-grow: 0;
            font-size: 24px;
            font-weight: bold;
            width: 2.25rem;
            height: 2.25rem;
            padding-left: 0.35rem;
            background-color: var(--color-current);
            border: 2px solid var(--color-secondary);
            border-radius: 5px;
        }
        .filler-btn {
            color: var(--color-tertiary);
            flex-grow: 1;
        }
        .points {
            padding: 1rem;
            justify-self: end;
        }
        .answer-container {
            display: flex;
            flex-direction: column;
            .team-password {
                align-self: flex-start;
            }
            .response-round-list {
                display: flex;
                flex-direction: column;
                width: 45%;
                min-width: 15rem;
            }
        }
        .megaround-alert {
            font-size: 14px;
            color: var(--color-primary);
            position: absolute;
        }
        .megaround {
            border: 2px solid var(--color-primary);
            border-radius: 10px;
            h3 {
                padding: 0.5rem;
                padding-bottom: 0;
            }
        }
    }
</style>
