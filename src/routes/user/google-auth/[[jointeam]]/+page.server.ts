import { error } from '@sveltejs/kit';
import { PRIVATE_GOOGLE_CLIENT_SECRET } from '$env/static/private';
import { PUBLIC_API_HOST } from '$env/static/public';
import * as cookie from 'cookie';
import { redirect } from '@sveltejs/kit';
import { getJwtPayload } from '$lib/utils';
import { googleAuthToken, googleAuthUrl } from '../../utils';
import type { Actions, PageServerLoad } from './$types';

export const load = (async ({ cookies, fetch, url }) => {
    const teamPassword = cookies.get('team_password');
    let next = cookies.get('next');

    const code = url.searchParams.get('code') || '';
    const authData = await googleAuthToken(code, PRIVATE_GOOGLE_CLIENT_SECRET);
    const apiResp = await fetch(`${PUBLIC_API_HOST}/user/google-auth`, {
        method: 'post',
        headers: {
            'content-type': 'application/json',
            Authorization: `Bearer ${authData.access_token}`
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

    if (teamPassword) {
        next = `/team/join?password=${teamPassword}`;
    } else if (!next) {
        next = jwtData?.staff_user ? '/host/choice' : '/team';
    }

    cookies.delete('team_password', { path: '/' });
    cookies.delete('next', { path: '/' });

    throw redirect(302, next);
}) satisfies PageServerLoad;

export const actions: Actions = {
    auth: async ({ cookies, request, url }) => {
        const data = await request.formData();
        const teamPassword = data.get('team_password') as string;
        const next = data.get('next') as string;
        const secureCookie = url.protocol === 'https:';

        if (teamPassword) {
            cookies.set('team_password', teamPassword, {
                path: '/',
                maxAge: 300,
                httpOnly: true,
                sameSite: 'lax',
                secure: secureCookie
            });
        }
        if (next) {
            cookies.set('next', next, {
                path: '/',
                maxAge: 300,
                httpOnly: true,
                sameSite: 'lax',
                secure: false
            });
        }

        const googleUrl = googleAuthUrl();

        throw redirect(302, googleUrl);
    }
};
