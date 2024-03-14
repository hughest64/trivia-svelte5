<script lang="ts">
    import { page } from '$app/stores';
    import stateManager from '$lib/state/utils.svelte';
    const { userState, getState } = stateManager;
    const data = $page.data;

    const hset = userState(data.user_data);
    const hget = getState('userState');
    // $inspect(hset?.active_team);
</script>

<slot />
