import { redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { LayoutServerLoad } from './$types';

const validateJwt = (token?: string): boolean => {
    if (!token) return false;
    // TODO: use a jwt lib to parse the token and check the exp,
    // if expired return false
    return true;
};

const apiMap = new Map([['/host/choice', '/user']]);

export const load: LayoutServerLoad = async ({ cookies, locals, request, fetch }) => {
    const url = new URL(request.url);
    const apiEndpoint = apiMap.get(url.pathname) || url.pathname;
    
    const jwtIsValid = validateJwt(cookies.get('jwt'));
    if (!jwtIsValid) throw redirect(302, `/user/logout?next=${url.pathname}`);

    let data = {};

    const response = await fetch(`${apiHost}${apiEndpoint}/`);

    if (response.ok) {
        const responseData = await response.json();
        data = { ...responseData, ...locals };

    } else if (url.pathname !== '/') {
        // TODO: this is only appropriate for unathorized requests we may need
        // to return an error to the page rather than redirecting in other cases
        throw redirect(302, `/?next=${url.pathname}`);
    }

    return data;
};
