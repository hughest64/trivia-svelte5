import { get } from 'svelte/store';
import { getFetchConfig } from '$lib/utils';
import { eventDataLoaded, setEventStores } from '$stores/event';

import type { EventData } from '$lib/types';
import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

export const load: PageLoad = async ({ fetch, url, params }) => {
    if (!get(eventDataLoaded)) {
        const fetchConfig = getFetchConfig('GET');
        const response = await fetch(`${apiHost}/event/${params.joincode}/`, fetchConfig);

        if (response.ok) {
            const data = (await response.json()) as EventData;
            data && setEventStores(data);
        } else {
            // TODO: checkStatusCode should have the true status code
            throw redirect(307, url.pathname);
        }
    }
};
