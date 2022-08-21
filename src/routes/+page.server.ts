// import { parseRequestHeaders } from '$lib/utils';
// import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

// TODO: holding off on this convert until the Actions api is updated
export const POST: Action = async ({ request }) => {
    const formData = await request.formData();

    console.log(formData.get('team-select'));
    // we may need the user's existing team as a hidden field
    // and compare it with the selected value, if the same reutrn location
    // else post to the api (setting the correct headers)
    // get the reponse then return location
    // NOTE: in the case of a new team, we need to update the user's active team store
    // so, we really need the abiltiy to return data to the page :sadface:
};
