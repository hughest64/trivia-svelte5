import { invalid } from '@sveltejs/kit';
import { PUBLIC_WEBSOCKET_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

const response: Action = async ({ fetch, request, params }) => {
    const data = Object.fromEntries((await request.formData()).entries());

    console.log(data);

    // we could check for a response id, if there isn't one post /create
    // if there is one patch (put?) to /response/<id>
    const response = await fetch(`${apiHost}/game/${params.joincode}/response/`, {
        method: 'POST',
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const resposeData = await response.json();
        return invalid(response.status, { error: resposeData.detail });
    }
};

export const actions = { response };