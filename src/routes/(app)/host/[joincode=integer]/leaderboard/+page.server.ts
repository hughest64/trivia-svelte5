import { env } from '$env/dynamic/public';
import { fail } from '@sveltejs/kit';
import type { Action } from './$types';

const updateleaderboard: Action = async ({ fetch, params }) => {
    const publicApiHost = env.PUBLIC_API_HOST;
    const response = await fetch(`${publicApiHost}/host/${params.joincode}/updatelb`, {
        method: 'post'
    });

    if (!response.ok) {
        const respJson = await response.json();
        console.log(respJson);
        return fail(response.status, { error: respJson.detail });
    }
    return { sucess: true };
};

export const actions = { updateleaderboard };
