<script context="module" lang="ts">
    import { get } from 'svelte/store'
    import { eventData } from '$stores/event'
    import type { Load } from '@sveltejs/kit';

    // conditonally fetch event data if the event store is empty
    export const load: Load = async ({ fetch, params }) => {
        const existingEventData = get(eventData);
        if (!existingEventData) {
            const response = await fetch(
                `http://localhost:8000/event/${params.joincode}/`,
                {
                    credentials: 'include',
                    headers: { accept: 'application/json' }
                }
            )

            if (response.status === 200) {
                const data = await response.json()
                eventData.set(data?.event_data)
            } else if (response.status === 404) {
                // TODO:
                // redirect to /game-select with a not found message?
            } else if (response.status === 403) {
                return {
                    // TODO: query string ?next=/game/${params.joincode}
                    redirect: '/user/login',
                    status: 302
                }
            }
        }

        return { status: 200 }
    }

</script>
<script lang="ts">
    // create socket connection here?
</script>

<slot />