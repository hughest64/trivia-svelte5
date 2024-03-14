<script lang="ts">
    import { page } from '$app/stores';
    import { getState, createState } from '$lib/state/utils.svelte';
    const data = $page.data;

    const hset = createState.userState(data.user_data);
    const hget = getState('userState');
    // $inspect(hset?.active_team);
</script>

<slot />
