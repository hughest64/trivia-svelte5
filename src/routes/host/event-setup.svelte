<script context="module" lang="ts">
    import { browser } from '$app/env'
    import type { Load } from '@sveltejs/kit';
    import type { GameSelectData, LocationSelectData, HostSelectData } from '$lib/types'
    
    export const load: Load = async({ fetch }) => {
        if (!browser) return { status: 200 }

        const response = await fetch(
            'http://localhost:8000/eventsetup',
            {
                credentials: 'include',
                headers: {
                    accept: 'application/json'
                }
            }
        ) 
        if (response.ok) {
            const data = await <HostSelectData>response.json()

            return {
                status: 200,
                props: data ? {
                    gameSelectData: data.game_select_data,
                    locationSelectData: data.location_select_data
                } : {}
            }
        }
        // TODO: actually check for a 4xx code
        // not a staff user
        return {
            redirect: '/game/team-select',
            status: 302
        }

    }
</script>

<script lang="ts">
    export let gameSelectData: GameSelectData
    export let locationSelectData: LocationSelectData

    $: console.log(gameSelectData)
    $: console.log(locationSelectData)

</script>
<h1>Event Setup</h1>