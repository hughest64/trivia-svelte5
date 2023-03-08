import { fail } from '@sveltejs/kit';
import { env } from '$env/dynamic/public';
import type { Action } from './$types';

const submitresponse: Action = async ({ fetch, request, params }) => {
    const data = Object.fromEntries((await request.formData()).entries());
    const apiHost = env.PUBLIC_API_HOST;
    const apiEndpoint = `${apiHost}/game/${params.joincode}/response`;

    const response = await fetch(apiEndpoint, {
        method: 'POST',
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const resposeData = await response.json();
        return fail(response.status, { error: resposeData.detail });
    }
    return data;
};

const joinevent: Action = async ({ fetch, params }) => {
    const apiHost = env.PUBLIC_API_HOST;
    const response = await fetch(`${apiHost}/game/join`, {
        method: 'post',
        body: JSON.stringify({
            joincode: params.joincode
        })
    });
    const responseData = await response.json();
    if (!response.ok) {
        // TODO: check for player_limit_exceeded reason and throw error if present
        return fail(responseData.status, { error: responseData.detail });
    }

    // throw redirect(303, `/game/${params.joincode}`);
    return { playerJoined: true };
};

export const actions = { submitresponse, joinevent };
