import { invalid, /* redirect */ } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action, /* PageServerLoad */ } from './$types';

// TODO: most likely deprecate this works but the user data we are checking doesn't
// necessarily refelct what the websocket receives on connection
// export const load: PageServerLoad = async ({ parent, })  => {
//     const data = <App.PageData>(await parent());
//     const userData = data.user_data;

//     // disallow /game endpoints if a user does not have an active set
//     if (!userData?.active_team_id) throw redirect(302, '/team');
// };

const response: Action = async ({ fetch, request, params }) => {
    const data = Object.fromEntries((await request.formData()).entries());
    const apiEndpoint = `${apiHost}/game/${params.joincode}/response/${data.response_id}`;

    const response = await fetch(apiEndpoint, {
        method: 'POST',
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const resposeData = await response.json();
        return invalid(response.status, { error: resposeData.detail });
    }
    return data;

};

export const actions = { response };