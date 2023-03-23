<script lang="ts">
    import { getStore } from '$lib/utils';
    import Entry from '$lib/leaderboards/Entry.svelte';
    import RoundSelector from '../RoundSelector.svelte';

    const leaderboard = getStore('leaderboard');

    type LbView = 'public' | 'host';
    let lbView: LbView = 'public';
</script>

<h1>Host - Leaderboard</h1>

<div class="btn-group">
    <button class="button button-primary" on:click={() => (lbView = 'host')}>Host View</button>
    <button class="button button-secondary" on:click={() => (lbView = 'public')}>Public View</button>
</div>

{#if $leaderboard.through_round && lbView === 'public'}
    <h3>Through Round {$leaderboard.through_round}</h3>
{/if}

<RoundSelector />

<!-- TODO: and nice slide transition would be cool here -->
{#if lbView === 'public'}
    <h4>Public Leaderboard</h4>
    <ul class="leaderboard-rankings">
        {#each $leaderboard.public_leaderboard_entries as entry}
            <Entry {entry} />
        {/each}
    </ul>
{:else}
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
