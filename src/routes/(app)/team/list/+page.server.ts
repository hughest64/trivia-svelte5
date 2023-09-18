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
    throw redirect(302, next);
};

// TODO: should this one not redirect but give the nice note as in the currrent app?
// it would contain a link to /game/join
const createTeam: Action = async ({ fetch, request, url }) => {
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
    throw redirect(302, next);
};

const joinTeam: Action = async ({ fetch, request, url }) => {
    const data = Object.fromEntries((await request.formData()).entries());

    const apiHost = PUBLIC_API_HOST;
    const response = await fetch(`${apiHost}/team/join`, {
        method: 'POST',
        body: JSON.stringify(data)
    });

    const responseData = await response.json();
    if (!response.ok) {
        return fail(response.status, { error: responseData.detail });
    }

    const next = url.searchParams.get('next') || '/game/join';
    throw redirect(302, next);
};

export const actions = { selectTeam, createTeam, joinTeam };
