<script lang="ts">
    import { onMount } from 'svelte'

    onMount (async () => {
        await fetch(
            'http://localhost:8000/user/logout/',
            {
                method: "POST",
                credentials: 'include'
            }
        )
        window.open('/user/login', '_self')
    })
</script>