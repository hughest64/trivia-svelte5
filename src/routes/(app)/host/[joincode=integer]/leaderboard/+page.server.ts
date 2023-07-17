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
        return fail(response.status, { error: respJson.detail });
    }
    return { sucess: true };
};

const revealanswers: Action = async ({ fetch, params }) => {
    const publicApiHost = env.PUBLIC_API_HOST;
    const response = await fetch(`${publicApiHost}/host/${params.joincode}/revealanswers`, {
        method: 'post'
    });

    if (!response.ok) {
        const respJson = await response.json();
        return fail(response.status, { error: respJson.detail });
    }

    return { success: true };
};

const finishgame: Action = async ({ fetch, params }) => {
    const publicApiHost = env.PUBLIC_API_HOST;
    const response = await fetch(`${publicApiHost}/host/${params.joincode}/finishgame`, {
        method: 'post'
    });

    if (!response.ok) {
        const respJson = await response.json();
        return fail(response.status, { error: respJson.detail });
    }

    return { success: true };
};

const updateteamname: Action = async ({ request }) => {
    const data = Object.fromEntries(await request.formData());
    console.log(data);
};

export const actions = { updateleaderboard, revealanswers, finishgame, updateteamname };
