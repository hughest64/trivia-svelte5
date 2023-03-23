<script lang="ts">
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import Entry from '$lib/leaderboards/Entry.svelte';
    import RoundSelector from '../RoundSelector.svelte';

    const leaderboard = getStore('leaderboard');

    type LbView = 'public' | 'host';
    let lbView: LbView = 'host';
</script>

<h1>Host - Leaderboard</h1>

<div class="btn-group">
    <button
        class="button {lbView === 'host' ? 'button-primary' : 'button-secondary'}"
        on:click={() => (lbView = 'host')}>Host View</button
    >
    <button
        class="button {lbView === 'public' ? 'button-primary' : 'button-secondary'}"
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

    <ul class="leaderboard-rankings">
        {#each $leaderboard.public_leaderboard_entries as entry}
            <Entry {entry} />
        {/each}
    </ul>
{:else}
    <!-- TOOD: button to sync leaderboards when not synced "Update Public View"
    NOTE: this also reveals the correct answer AND pts awarded to individual teams/players -->
    <form action="?/updateleaderboard" method="post" use:enhance>
        <button type="submit" class="button button-primary">Update Public View</button>
    </form>

    <h4>Host Leaderboard</h4>

    <ul class="leaderboard-rankings">
        {#each $leaderboard.host_leaderboard_entries as entry}
            <Entry {entry} />
        {/each}
    </ul>
{/if}

<style lang="scss">
    .btn-group {
        display: flex;
        width: 100%;
        justify-content: center;
    }
    ul {
        width: 100%;
    }
</style>
