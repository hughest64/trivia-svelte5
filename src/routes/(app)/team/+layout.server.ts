import { redirect } from '@sveltejs/kit';
import { handlePlayerAuth, sortUserTeams } from '$lib/utils';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async (loadEvent) => {
    const data = await handlePlayerAuth({ ...loadEvent, endPoint: '/user' });
    const activeTeamId = data.user_data?.active_team_id;
    const userTeams = data.user_data?.teams;

    // if a user lands on /team but does not belong to any teams, send them to /team/create
    const toPath = new URL(loadEvent.request.url).pathname;
    if (!userTeams?.length && toPath === '/team') {
        redirect(302, `/team/create${loadEvent.url.search}`);
    }

    // put the user's active team at the front
    if (data.user_data && activeTeamId && userTeams?.length) {
        const sortedTeams = sortUserTeams(userTeams, activeTeamId);
        if (sortedTeams) data.user_data.teams = sortedTeams;
    }

    return data;
};
