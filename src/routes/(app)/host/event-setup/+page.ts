// import { error } from '@sveltejs/kit';

import type { PageLoad } from './$types';

import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import { browser } from '$app/environment';

export const load: PageLoad = async ({ parent, fetch }) => {
    if (browser) {
        const data = await parent();
        const response = await fetch(`${apiHost}/eventsetup/`, 
            {
                method: 'GET',
                headers: data.fetchHeaders
            }
        );
    
        if (response.ok) {
            const responnseData = await response.json();
            // data && userdata.set(data.user_data);
    
            return {    
                gameSelectData: responnseData.game_select_data || [],
                locationSelectData: responnseData.location_select_data || []
            };
        }
        // TODO: checkStatusCode /throw redirect?
        // throw error(403);
    }
};
