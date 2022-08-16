import { getFetchConfig } from '$lib/utils';
import { get } from 'svelte/store';
import { redirect } from '@sveltejs/kit';
import { userdata } from '$stores/user';
import type { PageLoad } from './$types';
const apiHost = import { PUBLIC_API_HOST as apiHost } from '$env/static/public';;

// TODO: migration - new file +layout.ts however,
// use the new await parent() to check user data?
// really questioning the store set up for user data
export const load: PageLoad = async () => {
    const data = get(userdata);
    if (!data) {
        // if (!data) {
        const fetchConfig = getFetchConfig('GET');
        const response = await fetch(`${apiHost}/user/`, fetchConfig);

        if (response.ok) {
            const user_data = await response.json();
            user_data && userdata.set(user_data);
        }  else {
            throw redirect(307, '/user/login');
        }
    }
};
