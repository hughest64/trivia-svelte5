<script lang="ts">
    import { onMount } from 'svelte'
    const apiHost = import.meta.env.VITE_API_HOST

    onMount (async () => {
        await fetch(
            `${apiHost}/user/logout/`,
            {
                method: "POST",
                credentials: 'include'
            }
        )
        window.open('/user/login', '_self')
    })
</script>