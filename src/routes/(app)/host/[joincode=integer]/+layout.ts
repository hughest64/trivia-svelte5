// import { redirect } from '@sveltejs/kit';
import { getFetchConfig } from '$lib/utils';
// import type { EventData } from '$lib/types';
import type { LayoutLoad } from './$types';
import { error } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

export const load: LayoutLoad = async ({ fetch, params }) => {
    // const user = get(getUserStore());
    // if (user && !user.is_staff) {
    //     throw redirect(302, '/');
    // }
    // if (!get(eventDataLoaded)) {
    const fetchConfig = getFetchConfig('GET');
    const response = await fetch(`${apiHost}/host-event/${params.joincode}/`, fetchConfig);

    if (response.ok) {
        // const data = <EventData>await response.json();
        // data && setEventStores(data);
    } else {
        // TODO: checkStatusCode
        throw error(403);
    }
    // }
};
