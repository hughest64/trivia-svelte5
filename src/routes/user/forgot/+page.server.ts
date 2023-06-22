import { env } from '$env/dynamic/public';
import { fail, redirect } from '@sveltejs/kit';
import * as cookie from 'cookie';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
    if (locals.validtoken) {
        throw redirect(302, '/team');
    }
};

export const actions: Actions = {
    default: async ({ cookies, request, fetch }) => {
        let csrftoken = cookies.get('csrftoken') || '';
        // if a user came here directly (not via the forgot link) then we won't have a csrf token, let's get one
        if (!csrftoken) {
            const csrfResp = await fetch('/user/login');
            const csrfCookie = cookie.parse(csrfResp.headers.get('set-cookie') || '');
            csrftoken = csrfCookie?.csrftoken || '';
            cookies.set('csrftoken', csrftoken, {
                expires: new Date(csrfCookie.expires),
                path: '/',
                secure: false,
                sameSite: 'lax'
            });
        }

        const username = (await request.formData()).get('username');

        const resp = await fetch(`${env.PUBLIC_API_HOST}/user/forgot`, {
            method: 'POST',
            headers: {
                accept: 'application/json',
                'content-type': 'application/json',
                Cookie: `csrftoken=${csrftoken}`,
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ username })
        });
        if (resp.status === 403) {
            // TODO Possibly an actual log?
            console.error('no csrf token');
            return fail(403, { error: 'the server denied the request' });
        }

        return { info: 'If a user exists, you will receive an email with instructions to reset your password.' };
    }
};
