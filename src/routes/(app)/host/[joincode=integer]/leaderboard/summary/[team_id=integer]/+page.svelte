<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import RoundSelector from '../../../RoundSelector.svelte';
    import LeaderboardSummary from '$lib/leaderboards/LeaderboardSummary.svelte';

    const leaderboard_id = $page.params.team_id;
    const leaderboard = getStore('leaderboard');

    const entry = $leaderboard.host_leaderboard_entries?.find((entry) => entry.team_id === Number(leaderboard_id));
</script>

<h1>Leaderboard Summary</h1>

<RoundSelector />

<LeaderboardSummary {entry} />
