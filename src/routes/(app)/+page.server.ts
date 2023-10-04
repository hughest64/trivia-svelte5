import * as cookie from 'cookie';
import { fail, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST } from '$env/static/public';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, fetch, locals, url }) => {
    const apiHost = PUBLIC_API_HOST;
    const secureCookie = url.protocol === 'https:';

    if (locals.validtoken) throw redirect(302, locals.staffuser ? `/host/choice${url.search}` : `/team${url.search}`);

    try {
        // get a csrf token from the api
        const getResponse = await fetch(`${apiHost}/user/login/`);
        if (!getResponse.ok) {
            const getResponseData = await getResponse.json();
            return fail(getResponseData.status, { error: getResponseData.detail });
        }

        const csrfCookie = cookie.parse(getResponse.headers.get('set-cookie') || '');
        const csrftoken = csrfCookie?.csrftoken || '';

        cookies.set('csrftoken', csrftoken, {
            expires: new Date(csrfCookie.expires),
            path: '/',
            secure: Boolean(secureCookie),
            sameSite: 'lax'
        });
    } catch (e) {
        console.error('could not connect to', apiHost);
        return { loaderror: 'Error: Could Not Connect to the Server' };
    }
};
