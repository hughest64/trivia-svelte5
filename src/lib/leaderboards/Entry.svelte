<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import type { LeaderboardEntry, Response } from '$lib/types';

    export let entry: LeaderboardEntry;
    let responses: Response[] = [];

    const userStore = getStore('userData');

    let expanded = false;
    // TODO: if on game/ then consider the user's active team first
    $: expandable = !expanded;

    const handleExpand = async () => {
        if (responses) {
            expanded = !expanded;
            return;
        }

        // TODO: we probably want a loading state here
        const resp = await fetch(`${$page.url.pathname}/responses/${entry.team_id}`);
        // TODO: handle !resp.ok
        if (resp.ok) {
            responses = (await resp.json())?.responses || [];
        }

        // TODO: update a store w/ the teams responses and then set expanded
        expanded = !expanded;
    };
</script>

<!-- TODO expandable for a user's active team or host in url route
    - for players, clicking on a response navigates to that question in the event
    - svgs for 1/.5. && 0 pts
    - how to handle unanswered questions?
    - slide transition for displaying/hiding content
    - how to fetch team data (password, name updates, banning, etc) for the host
-->
<li class="leaderboard-entry-container">
    <div class="leaderboard-entry-meta">
        <button
            class="rank"
            class:expandable
            class:expanded
            on:click={handleExpand}
            style:border-bottom-right-radius={expanded ? '10px' : 0}
        >
            <h3>{entry.rank}</h3>
        </button>
        <!-- <h3 class="rank">{entry.rank}</h3> -->
        <h3 class="team-name">{entry.team_name}</h3>
        <h3 class="points">{entry.total_points}</h3>
    </div>

    {#if expanded}
        <div class="answer-container">
            <p class="team-password">Team Password: {entry.team_password}</p>
            <ul class="response-list">
                {#each responses || [] as response}
                    <li>{response.key} {response.points_awarded} {response.recorded_answer}</li>
                {/each}
            </ul>
        </div>
    {/if}
</li>

<style lang="scss">
    .leaderboard-entry-container {
        // display: flex;
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
        }
        .rank {
            justify-content: center;
            min-width: 3.5rem;
            padding: 1.25rem;
            background-color: var(--color-alt-black);
            color: var(--color-tertiary);
        }
        .expanded {
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
        .expandable {
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
            .response-list {
                display: flex;
                flex-direction: column;
            }
        }
    }
</style>
