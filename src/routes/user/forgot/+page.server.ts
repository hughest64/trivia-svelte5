import { env } from '$env/dynamic/public';
import type { Actions } from './$types';

export const actions: Actions = {
    default: async ({ request, fetch }) => {
        const username = (await request.formData()).get('username');

        const resp = await fetch(`${env.PUBLIC_API_HOST}/user/forgot`, {
            method: 'POST',
            headers: { accept: 'application/json', 'content-type': 'application/json' },
            body: JSON.stringify({ username })
        });
        console.log(await resp.json());
        // TODO: handle response back to the page
    }
};
