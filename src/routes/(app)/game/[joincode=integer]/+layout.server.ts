import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ depends, locals, parent, url }) => {
    depends('active:data');
    const data = <App.PageData>await parent();
    // for a logout if the jwt is not valid
    if (!locals.validtoken) throw redirect(303, `/user/logout?next=${url.pathname}`);
    
    // TODO: we may need to rethink this, like let the api handle it
    // disallow /game endpoints if a user does not have an active set
    // const userData = data.user_data;
    // if (!userData?.active_team_id) throw redirect(302, `/team?next=${url.pathname}`);

    return { ...data, ...locals };
};
