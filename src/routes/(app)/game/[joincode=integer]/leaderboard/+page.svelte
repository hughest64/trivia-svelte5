<script lang="ts">
    import { getStore } from '$lib/utils';
    import type { PublicLeaderboard } from '$lib/types';

    $: leaderboard = getStore<PublicLeaderboard>('publicLeaderboard');
</script>

<h1>Game - Leaderboard</h1>

<!-- TODO flesh this out so we have some elements/classes to look for in our leaderboard update test(s)-->
<pre>{JSON.stringify($leaderboard, null, 4)}</pre>
