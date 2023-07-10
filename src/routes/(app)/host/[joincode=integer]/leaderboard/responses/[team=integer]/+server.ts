import { env } from '$env/dynamic/public';
import type { RequestHandler } from './$types';

export const GET = (async ({ locals, url }) => {
    const resp = await fetch(`${env.PUBLIC_API_HOST}${url.pathname}`, {
        headers: locals.fetchHeaders
    });

    return resp;
}) satisfies RequestHandler;
