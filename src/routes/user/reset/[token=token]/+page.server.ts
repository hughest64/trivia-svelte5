import { env } from '$env/dynamic/public';
import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

// TODO: possibly a load function that redirects if the token isnt' valid?
// this would be alternate to the param checker

export const actions: Actions = {
    default: async ({ request, fetch, params }) => {
        const data = await request.formData();
        const { pass1, pass2 } = Object.fromEntries(data);

        if (pass1 !== pass2) {
            return fail(400, { error: 'Passwords do not match' });
        }

        const token = params.token;

        const resp = await fetch(`${env.PUBLIC_API_HOST}/user/reset`, {
            method: 'post',
            headers: { accept: 'application/json', 'content-type': 'application/json' },
            body: JSON.stringify({ pass1, pass2, token })
        });

        if (!resp.ok) {
            const respData = await resp.json();
            return fail(resp.status, { error: respData.detail });
        }

        throw redirect(301, '/team');
    }
};
