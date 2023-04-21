<script lang="ts">
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import Entry from '$lib/leaderboards/Entry.svelte';
    import RoundSelector from '../RoundSelector.svelte';

    const leaderboard = getStore('leaderboard');
    const roundStates = getStore('roundStates');
    // TODO: I'm not entirely sure this is what we want here
    // used for determining when to show the "Reveal Answers" button
    $: maxLockedRound = $roundStates.filter((rs) => rs.locked).sort((a, b) => b.round_number - a.round_number)[0];

    let lbView: 'public' | 'host' = 'host';
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
                <Entry {entry} />
            {/each}
        </ul>
    {:else}
        {#if maxLockedRound && !maxLockedRound?.revealed}
            <form action="?/revealanswers" method="post" use:enhance>
                <button id="reveal-button" class="button button-secondary">Reveal Answers</button>
            </form>
        {:else if !$leaderboard.synced}
            <form action="?/updateleaderboard" method="post" use:enhance>
                <button id="sync-button" type="submit" class="button button-primary">Update Public View</button>
            </form>
        {/if}

        <h4>Host Leaderboard</h4>

        <ul id="host-leaderboard-view" class="leaderboard-rankings">
            {#each $leaderboard.host_leaderboard_entries as entry}
                <Entry {entry} />
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
        width: 100vw;
    }
</style>
