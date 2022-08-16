<script lang="ts">
    import { onMount } from 'svelte';
    import { getFetchConfig } from '$lib/utils';
    import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

    onMount(async () => {
        const fetchConfig = getFetchConfig('POST');
        await fetch(`${apiHost}/user/logout/`, fetchConfig);
        window.open('/welcome', '_self');
    });
</script>
