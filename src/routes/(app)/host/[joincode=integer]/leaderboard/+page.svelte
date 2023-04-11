<script lang="ts">
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import Entry from '$lib/leaderboards/Entry.svelte';
    import RoundSelector from '../RoundSelector.svelte';

    const leaderboard = getStore('leaderboard');

    type LbView = 'public' | 'host';
    let lbView: LbView = 'host';
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
        {#if !$leaderboard.synced}
            <!-- TODO: perhaps one button that changes jobs is better than two buttons? i.e. reveal first the update
        maybe use a query param on the action to indicate what is what -->
            <div class="btn-group">
                <form action="?/revealanswers" method="post" use:enhance>
                    <button id="reveal-button" class="button button-secondary">Reveal Answers</button>
                </form>
                <form action="?/updateleaderboard" method="post" use:enhance>
                    <button id="sync-button" type="submit" class="button button-primary">Update Public View</button>
                </form>
            </div>
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
