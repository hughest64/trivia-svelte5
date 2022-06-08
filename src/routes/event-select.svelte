<script context="module" lang="ts">
    import { browser } from '$app/env'
    import type { Load } from '@sveltejs/kit';
    // NOTE: we shouldn't need these, as we can use a permissions class django side
    // import { get } from 'svelte/store'
    // import { userdata } from '../stores/user'
    import type { EventSelectData, LocationSelectData, HostSelectData } from '../stores/eventselect'
    
    export const load: Load = async({ fetch }) => {
        if (!browser) return { status: 200 }

        const response = await fetch(
            'http://localhost:8000/eventdata',
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
                eventSelectData: data.event_select_data,
                locationSelectData: data.location_select_data
            } : {}
        }
    }
</script>

<script lang="ts">
    export let eventSelectData: EventSelectData
    export let locationSelectData: LocationSelectData

    $: console.log(eventSelectData)
    $: console.log(locationSelectData)

</script>
<h1>Event Select</h1>