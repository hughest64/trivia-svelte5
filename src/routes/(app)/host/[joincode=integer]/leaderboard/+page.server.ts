import { env } from '$env/dynamic/public';
import { fail } from '@sveltejs/kit';
import type { Action } from './$types';
import { PUBLIC_API_HOST } from '$env/static/public';

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

const updateteamname: Action = async ({ request, fetch, params }) => {
    const data = Object.fromEntries(await request.formData());

    const response = await fetch(`${PUBLIC_API_HOST}/team/updateteamname`, {
        method: 'post',
        body: JSON.stringify({ ...data, joincode: params.joincode })
    });

    if (!response.ok) {
        const respJson = await response.json();
        return fail(response.status, { error: respJson.detail });
    }
    return { success: true };
};

const updatepointsadjustment: Action = async ({ request, fetch, params }) => {
    const data = Object.fromEntries(await request.formData());

    const response = await fetch(`${PUBLIC_API_HOST}/host/${params.joincode}/pointsadjustment`, {
        method: 'post',
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        // parse the reason and return fail
    }
    return { success: true };
};

export const actions = { updateleaderboard, revealanswers, finishgame, updateteamname, updatepointsadjustment };
