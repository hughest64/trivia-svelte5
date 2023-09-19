import * as cookie from 'cookie';
import { fail, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST } from '$env/static/public';
import { getJwtPayload } from '$lib/utils';
import type { Actions } from './$types';

// TODO:
// perhaps a load function should check for an existing jwt and redirect if it's valid, or remove it if it's not
// we should probably also have the api send a csrf cookie to handle the case of direct navigation
// (i.e, did't come from the log in page)

export const actions: Actions = {
    default: async ({ cookies, fetch, request, url }) => {
        const formData = await request.formData();
        const username = formData.get('username');
        const pass = formData.get('pass');
        const pass2 = formData.get('pass2');
        const email = formData.get('email');

        let body = '';
        if (formData.get('guest_user')) {
            body = JSON.stringify({ guest_user: true });
        } else {
            if (!username || !pass || !pass2 || !email) {
                return fail(400, { error: 'Please fill in all required fields' });
            }
            if (pass !== pass2) {
                return fail(400, { error: 'Passwords do not match!' });
            }

            body = JSON.stringify({ username, pass, pass2, email });
        }

        const csrftoken = cookies.get('csrftoken') || '';

        const apiHost = PUBLIC_API_HOST;
        const response = await fetch(`${apiHost}/user/create`, {
            method: 'post',
            headers: {
                accept: 'application/json',
                'content-type': 'application/json',
                Cookie: `csrftoken=${csrftoken}`,
                'X-CSRFToken': csrftoken
            },
            body
        });

        const respData = await response.json();
        if (!response.ok) {
            return fail(response.status, { error: respData.detail });
        }

        const secureCookie = url.protocol === 'https:';
        const responseCookies = response.headers.get('set-cookie') || '';
        const jwt = cookie.parse(responseCookies)?.jwt;
        let guestUser = false;
        let userCreated = true;
        if (jwt) {
            const jwtData = getJwtPayload(jwt);
            guestUser = !!jwtData.guest_user;
            userCreated = !!jwtData.user_created;
            const expires = new Date((jwtData.exp as number) * 1000);
            cookies.set('jwt', jwt, { path: '/', expires, httpOnly: true, secure: secureCookie });
        }

        let next = url.searchParams.get('next');
        if (!next) {
            // direct newly created guest users to the team creation page
            if (guestUser && userCreated) {
                next = '/team/create';
            } else {
                next = '/team';
            }
        }
        throw redirect(302, next);
    }
};
