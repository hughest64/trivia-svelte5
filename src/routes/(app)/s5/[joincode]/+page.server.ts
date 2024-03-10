import type { Actions } from './$types';

export const actions: Actions = {
    default: async ({ request, fetch }) => {
        const data = Object.fromEntries(await request.formData());
        console.log(data);
    }
};
