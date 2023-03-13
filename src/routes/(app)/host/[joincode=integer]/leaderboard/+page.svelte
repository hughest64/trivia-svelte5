<script lang="ts">
    import { getStore } from '$lib/utils';

    $: leaderboard = getStore('publicLeaderboard');
</script>

<h1>Host - Leaderboard</h1>

<pre>{JSON.stringify($leaderboard, null, 4)}</pre>
