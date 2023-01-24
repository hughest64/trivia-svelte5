import { error, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { LayoutServerLoad } from './$types';

const apiMap = new Map([
    ['/host/choice', '/user'],
    // TODO: should we keep this?
    ['/game/join', '/user']
]);

export const load: LayoutServerLoad = async ({ locals, url, fetch }) => {
    const apiEndpoint = apiMap.get(url.pathname) || url.pathname;

    if (!locals.validtoken) throw redirect(302, `/user/logout?next=${url.pathname}`);

    const response = await fetch(`${apiHost}${apiEndpoint}/`);

    let data = {};
    const pageData = await response.json();
    if (response.ok) {
        data = { ...pageData, ...locals };
    }

    // not authorized, redirect to log out to ensure cookies get deleted
    if (response.status === 401) {
        throw redirect(302, `/user/logout?next=${url.pathname}`);
    }
    // forbidden, redirect to a safe page
    if (response.status === 403) {
        if (pageData?.reason === 'join_required') {
            throw redirect(302, `/game/join?reason=${pageData.reason}`);
        }
        throw redirect(302, '/team');
    }
    // TODO: expand to handle other pages (/team, etc)
    // resolve the error page
    if (response.status === 404) {
        throw error(404, { message: pageData.detail, next: '/game/join' });
    }

    return data;
};
