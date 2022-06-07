<script context="module" lang="ts">
    import { browser } from '$app/env'
    import { teams } from '../stores/teams';
    // @ts-ignore
    export async function load({ fetch, session}) {
        // check session for teams
        // if no teams, fetch and set them
        // return based on what not
        teams.set(['a', 'b', 'c'])

        return { status: 200 }
    }
</script>
<script lang="ts">
    // import { session } from '$app/stores'
    $: userTeams = $teams
    $: console.log(userTeams)

    // bind team data from $session
    // function to post selected team and set as selected team in session data
</script>
<h1>Team Select</h1>