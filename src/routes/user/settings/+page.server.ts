import type { Actions, PageServerLoad } from './$types';
import { PUBLIC_API_HOST } from '$env/static/public';

export const load: PageServerLoad = async ({ fetch }) => {
    const apiResponse = await fetch(`${PUBLIC_API_HOST}/user`);
    const apiData = await apiResponse.json();
    if (!apiResponse.ok) {
        // handle error
    }
    return apiData;
};

export const actions: Actions = {
    username: async ({ request, fetch }) => {
        const data = Object.fromEntries(await request.formData());
        console.log(data);
    },
    password: async ({ request, fetch }) => {
        const data = Object.fromEntries(await request.formData());
        console.log(data);
    },
    email: async ({ request, fetch }) => {
        const data = Object.fromEntries(await request.formData());
        console.log(data);
    }
};
