import { invalid, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

export const selectTeam: Action = async ({  fetch, request, url }) => {
    const { selectedteam, currentteam } = Object.fromEntries((await request.formData()).entries());

    if (selectedteam !== currentteam) {
        const response = await fetch(`${apiHost}/teamselect/`, {
            method: 'POST',
            body: JSON.stringify({ team_id: selectedteam })
        });

        const responseData = await response.json();
        if (!response.ok) {
            return invalid(response.status, { error: responseData.detail });
        }
    }

    const next = url.searchParams.get('next') || '/game/join';
    throw redirect(302, next);
};

export const actions = {
    default: selectTeam,
};