import { fail } from '@sveltejs/kit';
import { PUBLIC_API_HOST } from '$env/static/public';
import type { Actions } from '../$types';

export const actions: Actions = {
    default: async ({ fetch, request, url }) => {
        const data = Object.fromEntries(await request.formData());

        const response = await fetch(`${[PUBLIC_API_HOST]}${url.pathname}/create`, {
            method: 'post',
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const respData = await response.json();
            return fail(response.status, { error: respData.detail });
        }

        return { success: true };
    }
};
