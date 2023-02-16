<script lang="ts">
    import { getStore } from '$lib/utils';
    import type { PublicLeaderboard } from '$lib/types';

    $: leaderboard = getStore<PublicLeaderboard>('publicLeaderboard');
</script>

<h1>Host - Leaderboard</h1>

<pre>{JSON.stringify($leaderboard, null, 4)}</pre>
