import { fail } from '@sveltejs/kit';
import { PUBLIC_API_HOST } from '$env/static/public';
import type { Actions } from './$types';

export const actions: Actions = {
    updatename: async ({ request, fetch, url }) => {
        const data = Object.fromEntries(await request.formData());
        const joincode = url.searchParams.get('joincode');
        Object.assign(data, { joincode });

        const response = await fetch(`${PUBLIC_API_HOST}/team/updateteamname`, {
            method: 'post',
            body: JSON.stringify(data)
        });
        const respData = await response.json();
        if (!response.ok) {
            return fail(response.status, { error: respData.detail });
        }

        return respData;
    }
};
