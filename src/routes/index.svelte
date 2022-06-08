
<script context="module" lang="ts">
    // import { browser } from '$app/env'
    import { get } from 'svelte/store';
    import { userdata } from '../stores/user';
    
    import type { Load } from '@sveltejs/kit';

    export const load: Load = async() => {
        const userData = get(userdata);
        const isStaff = userData?.is_staff

        return {
            // TODO: we may need to handle having no user data here as well
            // (redirect to '/user/login')
            redirect: isStaff ? '/host-or-play': '/team-select',
            status: 302
        }
    }
</script>