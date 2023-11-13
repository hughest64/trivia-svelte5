<script lang="ts">
    import { enhance } from '$app/forms';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import Entry from '$lib/leaderboards/Entry.svelte';
    import RoundSelector from '../RoundSelector.svelte';
    import type { LeaderboardEntry } from '$lib/types';

    const leaderboard = getStore('leaderboard');
    const rounds = getStore('rounds');
    const roundStates = getStore('roundStates');

    // show the reveal button if any locked rounds are not revealed
    $: lockedRounds = $roundStates.filter((rs) => rs.locked);
    $: revealed = lockedRounds.every((rd) => rd.revealed);
    $: completedRounds = $roundStates.filter((rs) => rs.locked && rs.revealed && rs.scored);
    $: gameComplete = completedRounds.length > 0 && $rounds.length === completedRounds.length;

    let lbView: 'public' | 'host' = 'host';

    const showTiebreakerButton = (entry: LeaderboardEntry, index: number) => {
        const hostEntries = $leaderboard?.host_leaderboard_entries || [];
        const previousTiedForRank = hostEntries[index - 1]?.rank;
        const nextTiedForRank = hostEntries[index + 1]?.rank;

        return Number(entry.rank) && entry.rank !== nextTiedForRank && entry.rank === previousTiedForRank;
    };
</script>

<div class="host-container flex-column">
    <h1>Host - Leaderboard</h1>

    <div class="btn-group">
        <button
            class="button {lbView === 'host' ? 'button-primary' : 'button-secondary'}"
            id="host-view"
            on:click={() => (lbView = 'host')}>Host View</button
        >
        <button
            class="button {lbView === 'public' ? 'button-primary' : 'button-secondary'}"
            id="public-view"
            on:click={() => (lbView = 'public')}>Public View</button
        >
    </div>

    <RoundSelector />

    <!-- TODO: and nice slide transition would be cool here -->
    {#if lbView === 'public'}
        {#if $leaderboard.through_round}
            <h4>Public Leaderboard Through Round {$leaderboard.through_round}</h4>
        {:else}
            <h4>Public Leaderboard</h4>
        {/if}

        <ul id="public-leaderboard-view" class="leaderboard-rankings">
            {#each $leaderboard.public_leaderboard_entries as entry}
                <Entry {entry} {lbView} />
            {/each}
        </ul>
    {:else}
        <!-- TODO: we might need to display both buttons rather than having a preference for revealed first -->
        {#if !revealed}
            <form action="?/revealanswers" method="post" use:enhance>
                <button id="reveal-button" class="button button-secondary">Reveal Answers</button>
            </form>
        {:else if !$leaderboard.synced}
            <form action="?/updateleaderboard" method="post" use:enhance>
                <button id="sync-button" type="submit" class="button button-primary">Update Public View</button>
            </form>
        {:else if gameComplete}
            <form action="?/finishgame" method="post" use:enhance>
                <button class="button button-primary" type="submit">Finish Game</button>
            </form>
        {/if}

        <h4>Host Leaderboard</h4>

        <ul id="host-leaderboard-view" class="leaderboard-rankings">
            {#each $leaderboard.host_leaderboard_entries || [] as entry, index}
                <Entry {entry} {lbView} />

                {#if showTiebreakerButton(entry, index)}
                    <div class="resolve-tiebreaker">
                        <a
                            href={`/host/${$page.params.joincode}/controlboard?tiebreaker=t`}
                            class=" button button-primary"
                        >
                            Resolve Tie
                        </a>
                    </div>
                {/if}
            {/each}
        </ul>
    {/if}
</div>

<style lang="scss">
    .btn-group {
        display: flex;
        width: 100%;
        justify-content: center;
    }
    ul {
        width: 100%;
    }
    form {
        width: calc(100vw - 2rem);
    }
    .resolve-tiebreaker {
        display: flex;
        justify-content: center;
    }
</style>
