<script lang="ts">
    import { page } from '$app/stores';
    import { createState, getState } from '$lib/state/utils.svelte';
    // import type { UserData } from '$lib/types';
    const data = $page.data;
    // console.log(data.user_data);
    const ud = createState('userState', data.user_data);
    const userState = getState('userState');
    $inspect(userState?.active_team);
</script>

<slot />
