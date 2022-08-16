import { getFetchConfig } from '$lib/utils';
import { get } from 'svelte/store';
import { userdata } from '$stores/user';
import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';

import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

export const load: PageLoad = async ({ fetch, url }) => {
    const data = get(userdata);

    if (!data) {
        const fetchConfig = getFetchConfig('GET');
        const response = await fetch(`${apiHost}/user/`, fetchConfig);

        if (response.ok) {
            userdata.set(await response.json());
        } else {
            // TODO: checkStatusCode for the real status code
            throw redirect(307, `/user/login?next=${url.pathname}`);
        }
    }
};
