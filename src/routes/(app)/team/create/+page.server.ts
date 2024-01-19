import { fail, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST } from '$env/static/public';
import type { Actions } from './$types';

export const actions: Actions = {
    createTeam: async ({ fetch, request, url }) => {
        const data = Object.fromEntries((await request.formData()).entries());

        const apiHost = PUBLIC_API_HOST;
        const response = await fetch(`${apiHost}/team/create`, {
            method: 'POST',
            body: JSON.stringify(data)
        });

        const responseData = await response.json();
        if (!response.ok) {
            return fail(response.status, { error: responseData.detail });
        }

        const next = url.searchParams.get('next') || '/game/join';
        // redirect(302, next);
        return responseData.team_data
    }
};
