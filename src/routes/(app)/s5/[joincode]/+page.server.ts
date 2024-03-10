import { PUBLIC_API_HOST } from '$env/static/public';
import type { Actions } from './$types';

export const actions: Actions = {
    default: async ({ request, fetch, params }) => {
        const data = Object.fromEntries(await request.formData());
        const resp = await fetch(`${PUBLIC_API_HOST}/host/${params.joincode}/s5/lock`, {
            method: 'post',
            body: JSON.stringify(data)
        });
        console.log(await resp.json());
    }
};
