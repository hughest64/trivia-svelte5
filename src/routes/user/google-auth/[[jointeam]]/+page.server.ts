import { error } from '@sveltejs/kit';
import { PRIVATE_GOOGLE_CLIENT_SECRET } from '$env/static/private';
import { PUBLIC_API_HOST } from '$env/static/public';
import * as cookie from 'cookie';
import { redirect } from '@sveltejs/kit';
import { getJwtPayload } from '$lib/utils';
import { googleAuthToken } from '../../utils';
import type { PageServerLoad } from './$types';

export const load = (async ({ cookies, fetch, url, params }) => {
    const code = url.searchParams.get('code') || '';

    const authData = await googleAuthToken(code, PRIVATE_GOOGLE_CLIENT_SECRET, !!params.jointeam);
    const csrftoken = cookies.get('csrftoken') || '';
    const apiResp = await fetch(`${PUBLIC_API_HOST}/user/google-auth`, {
        method: 'post',
        headers: {
            'content-type': 'application/json',
            Authorization: `Bearer ${authData.access_token}`,
            Cookie: `csrftoken=${csrftoken}`,
            'X-CSRFToken': csrftoken
        }
    });

    if (!apiResp.ok) {
        throw error(400, { message: 'Cannot authenticate with Google' });
    }

    const secureCookie = url.protocol === 'https:';
    const responseCookies = apiResp.headers.get('set-cookie') || '';
    const jwt = cookie.parse(responseCookies)?.jwt;

    if (!jwt) {
        throw error(400, { message: 'Cannot authenticate with Google' });
    }

    const jwtData = getJwtPayload(jwt);
    const expires = new Date((jwtData.exp as number) * 1000);
    cookies.set('jwt', jwt, { path: '/', expires, httpOnly: true, secure: secureCookie });

    const next = cookies.get('next') || (jwtData?.staff_user ? '/host/choice' : '/team');
    cookies.delete('next', { path: '/' });

    throw redirect(302, next);
}) satisfies PageServerLoad;
