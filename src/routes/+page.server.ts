// import { parseRequestHeaders } from '$lib/utils';
// import { get } from 'svelte/store';
// import { redirect } from '@sveltejs/kit';
// import { userdata } from '$stores/user';
import type { PageServerLoad } from './$types';
// import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

// TODO: deprecate the fucntion, but keep the file as it will likely contain a POST

export const load: PageServerLoad = async (/** { request } */) => {
    // const data = get(userdata);

    // // TODO: we should check for a jwt first, if no jwt, redirect to login right away
    // if (!data) {
    //     const headers = parseRequestHeaders(request);
    //     const response = await fetch(
    //         `${apiHost}/user/`,
    //         {
    //             method: 'GET',
    //             headers
    //         }
    //     );

    //     if (response.ok) {
    //         const user_data = await response.json();
    //         user_data && userdata.set(user_data);
    //     } else {
    //         throw redirect(307, '/user/login');
    //     }
    // }
};
