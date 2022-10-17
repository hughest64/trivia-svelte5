import { invalid } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

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