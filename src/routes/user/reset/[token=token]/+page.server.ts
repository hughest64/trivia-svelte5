import { env } from '$env/dynamic/public';
import type { Actions } from './$types';

export const actions: Actions = {
    default: async ({ request, fetch, params }) => {
        const data = await request.formData();
        const { pass1, pass2 } = Object.fromEntries(data);
        const token = params.token;
        console.log(pass1, pass2);
        console.log(token);
    }
};
