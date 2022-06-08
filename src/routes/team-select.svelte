<script context="module" lang="ts">
    import { browser } from '$app/env'
    import { get } from 'svelte/store'

    import { userdata, userteams } from '../stores/user';
    import type { UserTeam } from '../stores/user';
    import type { Load } from '@sveltejs/kit';

    export const load: Load = async({ fetch }) => {
        // use this technique to not needlessly make two server requests
        if (!browser) return { status: 200 }

        // TODO: don't proceed if no user name (actually, id)
        const username = get(userdata).username

        const response = await fetch(
            // url should append /<userid>
            'http://localhost:8000/team/',
            { credentials: 'include' }
        )
        // some weird issue with data format coming from DRF when
        // we run this server side
        if (response.ok && browser) {
            const data = await <UserTeam[]>response.json()
            userteams.set([...data])
        }

        return { status: 200 }
    }
</script>

<script lang="ts">
    $: userTeams = $userteams
    $: console.log(userTeams)

    // function to post selected team and set as selected team in session data
</script>

<h1>Team Select</h1>