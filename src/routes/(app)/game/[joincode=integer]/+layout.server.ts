import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals, parent, url })  => {
    const data = <App.PageData>(await parent());
    const userData = data.user_data;

    // for a logout if the jwt is not valid
    if (!locals.validtoken) throw redirect(303, `/user/logout?next=${url.pathname}`);

    // TODO: why is this broken + we need a message upon redirect
    // disallow /game endpoints if a user does not have an active set
    // if (!userData?.active_team_id) throw redirect(302, `/team?next=${url.pathname}`);
};