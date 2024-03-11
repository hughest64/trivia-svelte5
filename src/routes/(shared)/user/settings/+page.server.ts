import * as cookie from 'cookie';
import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { PUBLIC_API_HOST } from '$env/static/public';
import { getJwtPayload } from '$lib/utils';

export const load: PageServerLoad = async ({ fetch }) => {
    const apiResponse = await fetch(`${PUBLIC_API_HOST}/user`);
    const apiData = await apiResponse.json();
    if (!apiResponse.ok) {
        // handle error
    }
    return apiData;
};

export const actions: Actions = {
    auto_reveal_update: async ({ request, fetch, url }) => {
        const data = Object.fromEntries(await request.formData());
        const response = await fetch(`${PUBLIC_API_HOST}/user/set-auto-reveal`, {
            method: 'post',
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const respData = await response.json();
            return fail(response.status, { error: respData.detail });
        }

        return { success: true };
    },
    user_update: async ({ request, fetch, cookies, url }) => {
        // no need to send the password confirmation to the api, so pull it out
        const { password2, ...data } = Object.fromEntries(await request.formData());
        data.update_type = data.username ? 'username' : 'email';

        // validate passwords if applicable
        if (data.password) {
            data.update_type = 'password';
            if (data.password !== password2) {
                return fail(400, { error: { password: 'Passwords do not match!' } });
            }
        }

        const response = await fetch(`${PUBLIC_API_HOST}/user/update`, {
            method: 'post',
            body: JSON.stringify(data)
        });
        const respData = await response.json();

        if (!response.ok) {
            return fail(response.status, { error: respData.detail });
        }

        const secureCookie = url.protocol === 'https:';
        const responseCookies = response.headers.get('set-cookie') || '';
        const jwt = cookie.parse(responseCookies)?.jwt;

        if (jwt) {
            const jwtData = getJwtPayload(jwt);
            const expires = new Date((jwtData.exp as number) * 1000);
            cookies.set('jwt', jwt, { path: '/', expires, httpOnly: true, secure: secureCookie });
        }

        return { success: { msg: 'Your profile has been updated', username: data.username } };
    }
};
