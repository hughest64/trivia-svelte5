<script lang="ts">
    import { page } from '$app/stores';
    import { createState } from './stores.svelte';
    const data = $page.data;
    const userState = createState('userState', data?.user_data);
</script>

<slot />
