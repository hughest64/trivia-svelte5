import { fail, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import { handlePlayerAuth, sortUserTeams } from '$lib/utils';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async (loadEvent) => {
    const data = await handlePlayerAuth({ ...loadEvent, endPoint: '/user' });
    const activeTeamId = data.user_data?.active_team_id;
    const userTeams = data.user_data?.teams;

    // put the user's active team at the front
    if (data.user_data && activeTeamId && userTeams?.length) {
        const sortedTeams = sortUserTeams(userTeams, activeTeamId);
        if (sortedTeams) data.user_data.teams = sortedTeams;
    }

    return data;
};

const selectTeam: Action = async ({ fetch, request, url }) => {
    const { selectedteam, currentteam } = Object.fromEntries((await request.formData()).entries());
    if (selectedteam !== currentteam) {
        const response = await fetch(`${apiHost}/team/join`, {
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

// TODO: should this one not redirect but give the nice note as in the curdrent app?
// it would contain a link to /game/join
const createTeam: Action = async ({ fetch, request, url }) => {
    const data = Object.fromEntries((await request.formData()).entries());

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

const submitTeamPassord: Action = async ({ fetch, request, url }) => {
    const data = Object.fromEntries((await request.formData()).entries());

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

export const actions = { selectTeam, createTeam, submitTeamPassord };
