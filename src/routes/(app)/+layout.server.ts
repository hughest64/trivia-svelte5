import { redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { LayoutServerLoad } from './$types';

const apiMap = new Map([['/host/choice', '/user']]);

export const load: LayoutServerLoad = async ({ locals, request, fetch }) => {
    const url = new URL(request.url);
    const apiEndpoint = apiMap.get(url.pathname) || url.pathname;

    if (!locals.validtoken) throw redirect(302, `/user/logout?next=${url.pathname}`);

    const response = await fetch(`${apiHost}${apiEndpoint}/`);

    let data = {};
    if (response.ok) {
        const responseData = await response.json();
        data = { ...responseData, ...locals };
    }

    // not authorized, redirect to log out to ensure cookies get deleted
    if (response.status === 401) {
        throw redirect(302, `/user/logout?next=${url.pathname}`);
    }
    // forbidden, redirect to a safe page
    if (response.status === 403) {
        throw redirect(302, '/team');
    }

    return data;
};
