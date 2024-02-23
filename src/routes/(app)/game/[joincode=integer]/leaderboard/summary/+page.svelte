<script lang="ts">
    import { getStore } from '$lib/utils';
    import RoundSelector from '../../RoundSelector.svelte';
    import LeaderboardSummary from '$lib/leaderboards/LeaderboardSummary.svelte';

    const leaderboard = getStore('leaderboard');
    const userData = getStore('userData');
    $: entry = $leaderboard.public_leaderboard_entries.find((entry) => entry.team_id === $userData.active_team_id);
</script>

<h1>Leaderboard Summary</h1>

<!-- TODO: we need the same click logic as the actual lb, i.e. goto the game page -->
<RoundSelector />

<LeaderboardSummary bind:entry />
