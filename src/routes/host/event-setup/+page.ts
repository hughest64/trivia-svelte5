import { error } from '@sveltejs/kit';
import { userdata } from '$stores/user';
import { getFetchConfig } from '$lib/utils';

import type { PageLoad } from './$types';

const apiHost = import.meta.env.VITE_API_HOST;

export const load: PageLoad = async({ fetch }) => {
    const fetchConfig = getFetchConfig('GET');
    const response = await fetch(`${apiHost}/eventsetup/`, fetchConfig); 

    if (response.ok) {
        const data = await response.json();
        data && userdata.set(data.user_data);

        return {
            data: {
                gameSelectData: data.game_select_data || [],
                locationSelectData: data.location_select_data || []
            }
        };
    }
    // TODO: checkStatusCode /throw redirect?
    throw error(403);

};
