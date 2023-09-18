import { handlePlayerAuth, sortUserTeams } from '$lib/utils';
import type { PageServerLoad } from './$types';

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
