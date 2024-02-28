import { fail } from '@sveltejs/kit';
import { PUBLIC_API_HOST } from '$env/static/public';
import type { Actions } from './$types';

export const actions: Actions = {
    createTeam: async ({ fetch, request, url }) => {
        const data = Object.fromEntries((await request.formData()).entries());

        const teamname = data.team_name as string;
        if (teamname.trim().match(/^\d{4}$/)) {
            return fail(400, { error: 'Joincodes are not valid team names. Please enter a valid team name.' });
        }

        const apiHost = PUBLIC_API_HOST;
        const response = await fetch(`${apiHost}/team/create`, {
            method: 'POST',
            body: JSON.stringify(data)
        });

        const responseData = await response.json();
        if (!response.ok) {
            return fail(response.status, { error: responseData.detail });
        }

        return responseData.team_data;
    }
};
