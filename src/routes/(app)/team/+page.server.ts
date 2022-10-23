import { invalid, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import { sortUserTeams } from '$lib/utils';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ parent }) => {
    const data = <App.PageData>await parent();
    const activeTeamId = data.user_data?.active_team_id;
    const userTeams = data.user_data?.teams;

    // put the user's active team at the front
    if (data.user_data && activeTeamId && userTeams?.length) {
        const sortedTeams = sortUserTeams(userTeams, activeTeamId);
        if (sortedTeams) data.user_data.teams = sortedTeams;
    }
};

export const selectTeam: Action = async ({ fetch, request, url }) => {
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
    default: selectTeam
};
