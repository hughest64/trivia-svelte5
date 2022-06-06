
<script context="module" lang="ts">
    import { browser } from '$app/env'
    //@ts-ignore
    export async function load({ session }) {
        // running on the server doesn't update the csrf token properly
        if (!browser) {
            return { status: 200 }
        }
        const userData = session.data
        const isStaff = userData?.is_staff

        return {
            // TODO: we may need to handle having no user data here as well
            // (redirect to '/user/login')
            redirect: isStaff ? '/host-or-play': '/team-select',
            status: 302
        }
    }
</script>
<!-- <script>
    import { onMount } from 'svelte'
    import { goto } from '$app/navigation'
    import { session } from '$app/stores'

    $: userData = $session.data

    onMount(async() => {
        console.log('in on mount', $session)
    })
</script> -->
