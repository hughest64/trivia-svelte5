import { PUBLIC_GOOGLE_CLIENT_ID, PUBLIC_API_HOST } from '$env/static/public';
import { PRIVATE_GOOGLE_CLIENT_SECRET } from '$env/static/private';
import * as cookie from 'cookie';
import { redirect } from '@sveltejs/kit';
import { getJwtPayload } from '$lib/utils';
import type { RequestHandler } from './$types';
import type { JwtPayload } from '$lib/types';

export const GET = (async ({ cookies, fetch, url }) => {
    const code = url.searchParams.get('code');
    // TODO: handle if we don't have a code
    const body = {
        client_id: PUBLIC_GOOGLE_CLIENT_ID,
        client_secret: PRIVATE_GOOGLE_CLIENT_SECRET,
        redirect_uri: 'http://127.0.0.1:5173/user/google-auth',
        grant_type: 'authorization_code',
        code
    };

    const authResp = await fetch('https://oauth2.googleapis.com/token', {
        method: 'post',
        body: JSON.stringify(body)
    });
    // TODO:
    if (!authResp.ok) {
        // throw error
    }
    const authData = await authResp.json();

    const apiResp = await fetch(`${PUBLIC_API_HOST}/user/google-auth`, {
        method: 'post',
        headers: {
            'content-type': 'application/json',
            Authorization: `Bearer ${authData.access_token}`
        }
    });

    if (!apiResp.ok) {
        // TODO throw error
    }

    const secureCookie = url.protocol === 'https:';
    const responseCookies = apiResp.headers.get('set-cookie') || '';
    const jwt = cookie.parse(responseCookies)?.jwt;

    let jwtData: JwtPayload = {};
    // TODO: probably throw error if there isn't a jwt?, this should never happen
    // but it would be ultra confusing as the user would just land back at the log in page
    if (jwt) {
        jwtData = getJwtPayload(jwt);
        const expires = new Date((jwtData.exp as number) * 1000);
        cookies.set('jwt', jwt, { path: '/', expires, httpOnly: true, secure: secureCookie });
    }
    // TODO: how to handle other redirects, like a next param?
    const next = jwtData?.staff_user ? '/host/choice' : '/team';
    throw redirect(302, next);
}) satisfies RequestHandler;
