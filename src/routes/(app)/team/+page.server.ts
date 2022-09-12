import { invalid, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

export const selectTeam: Action = async ({ locals, request }) => {
    const { selectedteam, currentteam } = Object.fromEntries((await request.formData()).entries());

    if (selectedteam !== currentteam) {
        const response = await fetch(`${apiHost}/teamselect/`, {
            method: 'POST',
            headers: locals.fetchHeaders || {},
            body: JSON.stringify({ team_id: selectedteam })
        });

        const responseData = await response.json();
        if (!response.ok) {
            throw invalid(response.status, { error: responseData.detail });
        }
    }

    throw redirect(302, '/game/join');
};

export const actions = {
    selectTeam,
};