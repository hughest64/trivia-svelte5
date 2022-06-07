
<script context="module" lang="ts">
    import { browser } from '$app/env'
    import { get } from 'svelte/store';
    import { userdata } from '../stores/user';
    // import type { UserData } from '../stores/user';
    import type { Load } from '@sveltejs/kit';

    export const load: Load = async() => {
        // running on the server doesn't update the csrf token properly
        // if (browser) {
        //     return { status: 200 }
        // }
        const userData = get(userdata);
        console.log(userData)
        // const userData = $userdata.username
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
