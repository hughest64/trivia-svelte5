<script context="module" lang="ts">
    // @ts-ignore
    export async function load({ fetch }) {
        await fetch(
            'http://localhost:8000/user/logout/',
            {
                method: "POST",
                credentials: 'include'
            }
        )

        return {
            status: 302,
            redirect: '/user/login'
        }
    }
</script>