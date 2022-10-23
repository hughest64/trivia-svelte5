import { invalid, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ parent }) => {
    const data = <App.PageData>(await parent());
    const activeTeamId = data.user_data?.active_team_id; 
    const userTeams = data.user_data?.teams;
    // TODO: I think we can do better, right not we have to do an extra request from host/choice
    // to get this to run, map we can invalidate somehow?
    // put the user's active team at the front
    if (data.user_data && activeTeamId && userTeams?.length) {
        const activeTeamIndex = userTeams.findIndex((team) => team.id === activeTeamId);
        if (activeTeamIndex) {
            const updatedTeams = [...userTeams];
            const activeTeam = updatedTeams.splice(activeTeamIndex, 1)[0];

            data.user_data.teams = [activeTeam, ...updatedTeams];
        }
    }    
};

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