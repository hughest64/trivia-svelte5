import { env } from '$env/dynamic/public';
import type { Actions } from './$types';

export const actions: Actions = {
    default: async ({ request, fetch }) => {
        const username = (await request.formData()).get('username');

        await fetch(`${env.PUBLIC_API_HOST}/user/forgot`, {
            method: 'POST',
            headers: { accept: 'application/json', 'content-type': 'application/json' },
            body: JSON.stringify({ username })
        });
        return { info: 'If a user exists, you will receive an email with instructions to reset your password.' };
    }
};
