import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

// NOTE: in the case of a new team, we need to update the user's active team store
// so, we really need the abiltiy to return data to the page, however the userdata is
// currently fetched separately after the redirect so it is updated via that. We probably
// need to monitor this and verify it still works that way after the actions api changes
export const POST: Action = async ({ locals, request }) => {
    const { selectedteam, currentteam } = Object.fromEntries((await request.formData()).entries());

    if (selectedteam !== currentteam) {
        const response = await fetch(
            `${apiHost}/teamselect/`,
            {
                method: 'POST',
                headers: locals.fetchHeaders || {},
                body: JSON.stringify({ team_id: selectedteam })
            }
        );
        const responseData = await response.json();
    
        if (!response.ok) {
            return { errors: { message: responseData.detail } };
        }
    }
    return {
        location: '/game/join'
    };
       

};
