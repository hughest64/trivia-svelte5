<script context="module" lang="ts">
    import { checkStatusCode, getFetchConfig } from '$lib/utils';
    import { get } from 'svelte/store';
    import { setEventStores, eventDataLoaded } from '$stores/event';
    import { userdata } from '$stores/user';
    import type { EventData } from '$lib/types';
    import type { Load } from '@sveltejs/kit';
    const apiHost = import.meta.env.VITE_API_HOST;

    export const load: Load = async ({ fetch, params }) => {
        const user = get(userdata);
        if (user && !user.is_staff) {
            return { redirect: '/', status: 302 };
        }
        if (!get(eventDataLoaded)) {
            const fetchConfig = getFetchConfig('GET');
            const response = await fetch(`${apiHost}/host-event/${params.joincode}/`, fetchConfig);

            if (response.ok) {
                const data = <EventData>(await response.json());
                data && setEventStores(data);
            } else {
                return checkStatusCode(response);
            }
        }
        return { status: 200 };
    };
</script>

<script lang="ts">
    import Socket from '$lib/Socket.svelte';
</script>

<Socket />

<slot />
