<script lang="ts">
    import { getStore } from '$lib/utils';
    import Entry from '$lib/leaderboards/Entry.svelte';
    import RoundSelector from '../RoundSelector.svelte';

    const leaderboard = getStore('leaderboard');
</script>

<h1>Team Standings</h1>

{#if $leaderboard.through_round}
    <h3>Through Round {$leaderboard.through_round}</h3>
{/if}

<RoundSelector />

<ul class="leaderboard-rankings">
    {#each $leaderboard.public_leaderboard_entries as entry}
        <Entry {entry} />
    {/each}
</ul>

<style lang="scss">
    ul {
        width: 100%;
    }
</style>
