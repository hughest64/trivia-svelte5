import { redirect } from '@sveltejs/kit';
import { getFetchConfig } from '$lib/utils';
import { get } from 'svelte/store';
import { setEventStores, eventDataLoaded } from '$stores/event';
import { userdata } from '$stores/user';
import type { EventData } from '$lib/types';
import type { PageLoad } from '@sveltejs/kit';
import { error } from '@sveltejs/kit';
const apiHost = import { PUBLIC_API_HOST as apiHost } from '$env/static/public';;

export const load: PageLoad = async ({ fetch, params }) => {
    const user = get(userdata);
    if (user && !user.is_staff) {
        throw redirect(302, '/');
    }
    if (!get(eventDataLoaded)) {
        const fetchConfig = getFetchConfig('GET');
        const response = await fetch(`${apiHost}/host-event/${params.joincode}/`, fetchConfig);

        if (response.ok) {
            const data = <EventData>(await response.json());
            data && setEventStores(data);
        } else {
            // TODO: checkStatusCode
            throw error(403);
        }
    }
};
