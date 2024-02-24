<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import RoundSelector from '../../../RoundSelector.svelte';
    import LeaderboardSummary from '$lib/leaderboards/LeaderboardSummary.svelte';

    const leaderboard_id = $page.params.team_id;
    const leaderboard = getStore('leaderboard');

    $: entry = $leaderboard.host_leaderboard_entries?.find((entry) => entry.team_id === Number(leaderboard_id));
</script>

<h1>Leaderboard Summary</h1>

<RoundSelector />

<LeaderboardSummary bind:entry />

<style lang="scss">
    :global(main .answer-container),
    h1 {
        padding: 0 1rem;
    }
</style>
