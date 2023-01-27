import { fail } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

const submitresponse: Action = async ({ fetch, request, params }) => {
    const data = Object.fromEntries((await request.formData()).entries());
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

export const actions = { submitresponse };
