<script lang="ts">
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import { getStore, respsByround, splitQuestionKey } from '$lib/utils';
    import EditTeamName from './icons/EditTeamName.svelte';
    import RoundResponses from './RoundResponses.svelte';
    import type { LeaderboardEntry } from '$lib/types';

    // TODO:
    // warning text for tiebreakers
    // - how to fetch team data (name updates, banning, etc) for the host
    // - team name editable for host

    export let entry: LeaderboardEntry;
    export let lbView: 'public' | 'host' = 'public';

    $: teamName = entry.team_name;

    const userStore = getStore('userData');
    const isPlayerEndpoint = $page.url.pathname.startsWith('/game');

    $: isPlayerTeamEntry = entry.team_id === $userStore.active_team_id;
    $: expandable = (!isPlayerEndpoint && lbView === 'host') || (isPlayerEndpoint && isPlayerTeamEntry);

    const rounds = getStore('rounds');
    const roundStates = getStore('roundStates');
    const teamResponseStore = getStore('responseData');

    $: responses = (expandable && $teamResponseStore) || [];
    $: groupedResps = respsByround(responses, $rounds, $roundStates);

    let expanded = false;
    $: collapsed = !expandable ? null : !expanded;

    let fetched = false;
    const handleExpand = async () => {
        if (!expandable) return;

        if (isPlayerEndpoint || fetched) {
            expanded = !expanded;
            return;
        }

        // TODO: we probably want a loading state here
        const resp = await fetch(`${$page.url.pathname}/responses/${entry.team_id}`);
        // TODO: handle !resp.ok
        if (resp.ok) {
            responses = (await resp.json())?.responses || [];
            fetched = true;
        }

        expanded = !expanded;
    };
    let nameEditable = false;
</script>

<li class="leaderboard-entry-container">
    <div class="leaderboard-entry-meta">
        <button class="rank" class:collapsed class:expanded on:click={handleExpand}>
            <h3>{entry.rank}</h3>
        </button>

        <div class="team-name" class:grow={!expanded}>
            {#if !expanded}
                <button on:click={handleExpand}>
                    <h3>{teamName}</h3>

                    <!-- TODO: add condition for is second half?-->
                    {#if (isPlayerTeamEntry || !isPlayerEndpoint) && !entry.megaround}
                        <span class="megaround-alert">!Mega Round</span>
                    {/if}
                </button>
            {:else}
                <form action="">
                    {#if nameEditable}
                        <input
                            on:click={() => {
                                if (!nameEditable) handleExpand();
                            }}
                            type="text"
                            name="team_name"
                            bind:value={teamName}
                        />
                    {:else}
                        <h3>{teamName}</h3>
                    {/if}
                </form>
            {/if}
        </div>

        {#if expanded}
            <button class="edit-teamname" on:click={() => (nameEditable = !nameEditable)}>
                <EditTeamName />
            </button>
        {/if}

        <button class="points" on:click={handleExpand}><h3>{entry.total_points}</h3></button>
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
            input {
                font-size: 1.25rem;
                font-weight: bold;
                font-family: 'Montserrat';
                padding: 0.3rem;
            }
            button {
                position: relative;
                text-align: left;
            }
        }
        .edit-teamname {
            margin: 0;
            padding: 0;
            flex-grow: 1;
            text-align: left;
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
