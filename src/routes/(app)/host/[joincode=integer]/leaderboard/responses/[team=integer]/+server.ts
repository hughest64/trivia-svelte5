import { PUBLIC_API_HOST } from '$env/static/public';
import type { RequestHandler } from './$types';

export const GET = (async ({ locals, url }) => {
    const resp = await fetch(`${PUBLIC_API_HOST}${url.pathname}`, {
        headers: locals.fetchHeaders
    });

    return resp;
}) satisfies RequestHandler;
