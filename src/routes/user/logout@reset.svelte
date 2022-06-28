<script lang="ts">
    import { onMount } from 'svelte'
    import { getFetchConfig } from '$lib/utils'
    const apiHost = import.meta.env.VITE_API_HOST

    onMount( async () => {
        const fetchConfig = getFetchConfig("POST")
        await fetch(`${apiHost}/user/logout/`, fetchConfig)
        window.open('/user/login', '_self')
    })
</script>