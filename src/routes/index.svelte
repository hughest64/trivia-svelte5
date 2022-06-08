<script>
    import { onMount } from 'svelte'
    import { goto } from '$app/navigation';
    import { userdata } from '../stores/user';

    onMount(async () => {
        // TODO: if no user data at all, go to login, but I don't think that will occur
        $userdata.is_staff ? goto('/host-or-play') : goto('/team-select')
    })
</script>