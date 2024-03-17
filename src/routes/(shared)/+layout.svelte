<script lang="ts">
    import { page } from '$app/stores';
    import { createState } from '$lib/state/utils.svelte';
    import type { UserData } from '$lib/types';
    const data = $page.data;

    let userData = createState.userState(data.user_data || ({} as UserData));
    createState.eventHandler(data);
</script>

<slot />
