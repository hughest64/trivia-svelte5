<script lang="ts">
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import { getStore, respsByround } from '$lib/utils';
    import RoundResponses from './RoundResponses.svelte';
    import type { LeaderboardEntry } from '$lib/types';

    // TODO:
    // - for players, clicking on a response navigates to that question in the event
    // - svgs for 1/.5. && 0 pts
    // - how to fetch team data (name updates, banning, etc) for the host
    // - team name editable for host

    export let entry: LeaderboardEntry;
    export let lbView: 'public' | 'host' = 'public';

    const userStore = getStore('userData');
    const isPlayerEndpoint = $page.url.pathname.startsWith('/game');

    $: isPlayerTeamEntry = entry.team_id === $userStore.active_team_id;
    $: expandable = (!isPlayerEndpoint && lbView === 'host') || (isPlayerEndpoint && isPlayerTeamEntry);

    const rounds = getStore('rounds');
    const roundStates = getStore('roundStates');
    $: roundsToShow = $rounds.filter((rd) => $roundStates.find((rs) => rs.round_number === rd.round_number)?.locked);

    const teamResponseStore = getStore('responseData');

    $: responses = (expandable && $teamResponseStore) || [];
    $: groupedResps = respsByround(responses, roundsToShow);

    let expanded = false;
    $: collapsed = !expandable ? null : !expanded;

    const handleExpand = async () => {
        if (!expandable) return;

        // TODO: just add "fetched" variable - set to true if false then fetch, else don't fetch if true
        // this could work as an object in a store (set higher up in context) to avoid re-fetching after navigation
        // combine the if's w/ something like if (isPlayerEndpint || fetched) // toggle and return
        if (responses?.length > 0) {
            expanded = !expanded;
            return;
        }
        if (isPlayerEndpoint) return;

        // TODO: we probably want a loading state here
        const resp = await fetch(`${$page.url.pathname}/responses/${entry.team_id}`);
        // TODO: handle !resp.ok
        if (resp.ok) {
            responses = (await resp.json())?.responses || [];
        }

        expanded = !expanded;
    };
</script>

<li class="leaderboard-entry-container">
    <button class="leaderboard-entry-meta" on:click={handleExpand}>
        <div class="rank" class:collapsed class:expanded>
            <h3>{entry.rank}</h3>
        </div>
        <h3 class="team-name">{entry.team_name}</h3>
        <h3 class="points">{entry.total_points}</h3>
    </button>

    {#if expanded}
        <div transition:slide class="answer-container">
            <p class="team-password">Team Password: {entry.team_password}</p>
            <ul class="response-round-list">
                {#each groupedResps || [] as group}
                    <li><RoundResponses roundResps={group} /></li>
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
            flex-grow: 1;
            margin: 0.5rem 0;
            padding: 0 1rem;
            text-align: left;
        }
        .points {
            padding: 1rem;
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
    }
</style>
