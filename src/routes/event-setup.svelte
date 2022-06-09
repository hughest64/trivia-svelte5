<script context="module" lang="ts">
    import { browser } from '$app/env'
    import type { Load } from '@sveltejs/kit';
    // NOTE: we shouldn't need these, as we can use a permissions class django side
    // import { get } from 'svelte/store'
    // import { userdata } from '../stores/user'
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
        let data: HostSelectData = {};
        if (response.ok) {
            data = await response.json()
        }

        return {
            status: 200,
            props: data ? {
                gameSelectData: data.game_select_data,
                locationSelectData: data.location_select_data
            } : {}
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