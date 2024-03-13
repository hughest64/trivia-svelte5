<script lang="ts">
    import { page } from '$app/stores';
    import { UserState, getState, createState } from './stores.svelte';
    $: data = $page.data;
    $: console.log(data.user_data);

    const userState = createState('userState', data.user_data);
</script>

<slot />
