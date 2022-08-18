// import { parseRequestHeaders } from '$lib/utils';
// import { get } from 'svelte/store';
// import { userdata } from '$stores/user';
// import type { UserData } from '$stores/user';
// import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

// import { PUBLIC_API_HOST as apiHost } from '$env/static/public';

// TODO: deprecate this function, but keep the file as it will likely contain a POST function

export const load: PageServerLoad = async (/** { request, url } */) => {
    // let data: UserData = get(userdata);
    // userdata && console.log('user', data?.username);
    // // console.log(data);

    // // TODO: if there is data, but no activeteamid, redirect to /, can we have an error with it?
    
    // // TODO: we should check for a jwt first, if no jwt, redirect to login right away
    // if (!data) {
    //     console.log('fetching');
    //     const headers = parseRequestHeaders(request);
    //     const response = await fetch(
    //         `${apiHost}/user/`,
    //         {
    //             method: 'GET',
    //             headers
    //         }
    //     );

    //     if (response.ok) {
    //         data = await response.json();
    //         userdata.set(data);
    //     } else {
    //         // TODO: checkStatusCode for the real status code
    //         throw redirect(307, `/user/login?next=${url.pathname}`);
    //     }
    // }
    // return { ...data };
};
