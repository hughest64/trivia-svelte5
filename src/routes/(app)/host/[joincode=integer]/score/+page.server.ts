import { PUBLIC_API_HOST } from '$env/static/public';
import { fail } from '@sveltejs/kit';
import type { Action } from './$types';

const updateresponse: Action = async ({ fetch, request, params }) => {
    const data = Object.fromEntries((await request.formData()).entries());

    const apiHost = PUBLIC_API_HOST;
    const response = await fetch(`${apiHost}/host/${params.joincode}/score`, {
        method: 'post',
        body: JSON.stringify(data)
    });

    const responseData = await response.json();
    if (!response.ok) {
        return fail(response.status, responseData.detail);
    }
    return { success: true };
};

const revealanswers: Action = async ({ fetch, params }) => {
    const publicApiHost = PUBLIC_API_HOST;
    const response = await fetch(`${publicApiHost}/host/${params.joincode}/revealanswers`, {
        method: 'post'
    });

    if (!response.ok) {
        const respJson = await response.json();
        return fail(response.status, { error: respJson.detail });
    }

    return { success: true };
};

export const actions = { updateresponse, revealanswers };
