import { PRIVATE_GITHUB_CLIENT_SECRET } from '$env/static/private';
import { env } from '$env/dynamic/public';
import { getJwtPayload } from '$lib/utils';
import { githubAuthToken } from '../utils';
import { error, redirect } from '@sveltejs/kit';
import * as cookie from 'cookie';
import type { RequestHandler } from './$types';

export const GET = (async ({ cookies, fetch, url }) => {
    const code = url.searchParams.get('code') || '';

    const authData = await githubAuthToken(code, PRIVATE_GITHUB_CLIENT_SECRET);
    const csrftoken = cookies.get('csrftoken') || '';
    const apiResp = await fetch(`${env.PUBLIC_API_HOST}/user/github-auth`, {
        method: 'post',
        headers: {
            'content-type': 'application/json',
            Authorization: `token ${authData.access_token}`,
            Cookie: `csrftoken=${csrftoken}`,
            'X-CSRFToken': csrftoken
        }
    });

    if (!apiResp.ok) {
        throw error(400, { message: 'Cannot authenticate with Github' });
    }

    const secureCookie = url.protocol === 'https:';
    const responseCookies = apiResp.headers.get('set-cookie') || '';
    const jwt = cookie.parse(responseCookies)?.jwt;

    if (!jwt) {
        throw error(400, { message: 'Cannot authenticate with Github' });
    }

    const jwtData = getJwtPayload(jwt);
    const expires = new Date((jwtData.exp as number) * 1000);
    cookies.set('jwt', jwt, { path: '/', expires, httpOnly: true, secure: secureCookie });

    const next = cookies.get('next') || (jwtData?.staff_user ? '/host/choice' : '/team');
    cookies.delete('next', { path: '/' });

    throw redirect(302, '/team');
}) satisfies RequestHandler;
