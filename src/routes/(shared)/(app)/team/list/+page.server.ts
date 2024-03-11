import { fail, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST } from '$env/static/public';
import type { Action } from './$types';

const selectTeam: Action = async ({ fetch, request, url }) => {
    const { selectedteam, currentteam } = Object.fromEntries((await request.formData()).entries());
    const apiHost = PUBLIC_API_HOST;
    if (selectedteam !== currentteam) {
        const response = await fetch(`${apiHost}/team/select`, {
            method: 'POST',
            body: JSON.stringify({ team_id: selectedteam })
        });

        const responseData = await response.json();
        if (!response.ok) {
            return fail(response.status, { error: responseData.detail });
        }
    }

    const next = url.searchParams.get('next') || '/game/join';
    redirect(302, next);
};

export const actions = { selectTeam };
