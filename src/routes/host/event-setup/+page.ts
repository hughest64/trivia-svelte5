import { userdata } from '$stores/user';
import { checkStatusCode, getFetchConfig } from '$lib/utils';

import type { PageLoad } from '@sveltejs/kit';
import type { GameSelectData, LocationSelectData } from '$lib/types';

const apiHost = import.meta.env.VITE_API_HOST;

export const load: PageLoad = async({ fetch }) => {
    // if (!browser) {
    //     return { status: 200}
    // }
    const fetchConfig = getFetchConfig('GET');
    const response = await fetch(`${apiHost}/eventsetup/`, fetchConfig); 

    if (response.ok) {
        const data = await response.json();
        data && userdata.set(data.user_data);

        throw new Error("@migration task: Migrate this return statement (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292693)");
        return {
            status: 200,
            props: {
                gameSelectData: data.game_select_data || [],
                locationSelectData: data.location_select_data || []
            }
        };
    }
    throw new Error("@migration task: Migrate this return statement (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292693)");
    return checkStatusCode(response);

};
