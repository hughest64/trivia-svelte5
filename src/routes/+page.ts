import { browser } from '$app/env';
import { getFetchConfig } from '$lib/utils';
import { get } from 'svelte/store';
import { error } from '@sveltejs/kit';
import { userdata } from '$stores/user';
import type { PageLoad } from '@sveltejs/kit';
const apiHost = import.meta.env.VITE_API_HOST;

// TODO: migration - new file +layout.ts however,
// use the new await parent() to check user data?
// really questioning the store set up for user data
export const load: PageLoad = async () => {
    const data = get(userdata);
    if (!data && browser) {
        // if (!data) {
        const fetchConfig = getFetchConfig('GET');
        const response = await fetch(`${apiHost}/user/`, fetchConfig);

        if (response.ok) {
            const user_data = await response.json();
            user_data && userdata.set(user_data);
        } else {
            // TODO: modify checkStatusCode to have a reason?
            throw error(403);
        }
    }
};
