<script lang="ts">
    import { getStore } from '$lib/utils';
    import RoundSelector from '../../RoundSelector.svelte';
    import LeaderboardSummary from '$lib/leaderboards/LeaderboardSummary.svelte';

    const leaderboard = getStore('leaderboard');
    const userData = getStore('userData');
    // const entry = $leaderboard.public_leaderboard_entries[0];
    const entry = $leaderboard.public_leaderboard_entries.find((entry) => entry.team_id === $userData.active_team_id);
    $: console.log($leaderboard.public_leaderboard_entries);
    $: console.log($userData);
</script>

<h1>Leaderboard Summary</h1>

<RoundSelector />

<LeaderboardSummary {entry} />
