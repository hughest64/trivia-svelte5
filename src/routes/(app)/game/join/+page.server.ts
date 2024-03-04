import { fail, redirect } from '@sveltejs/kit';
import { handlePlayerAuth } from '$lib/utils';
import { PUBLIC_API_HOST } from '$env/static/public';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async (loadEvent) => {
    return handlePlayerAuth({ ...loadEvent, endPoint: '/user' });
};

const checkevent: Action = async ({ fetch, request }) => {
    const formData = await request.formData();
    const joincode = formData.get('joincode');

    const apiHost = PUBLIC_API_HOST;
    const response = await fetch(`${apiHost}/game/check/${joincode}`);
    const responseData = await response.json();
    if (!response.ok) {
        return fail(responseData.status, { error: responseData.detail, reason: responseData.reason || 'generic' });
    }
    return responseData;
};

const joinevent: Action = async ({ fetch, request }) => {
    const formData = await request.formData();
    const joincode = formData.get('joincode');

    if (!joincode) {
        return { errors: { message: 'Please Enter a Join Code' } };
    }
    const apiHost = PUBLIC_API_HOST;
    const response = await fetch(`${apiHost}/game/join`, {
        method: 'post',
        body: JSON.stringify({ joincode: joincode })
    });
    const responseData = await response.json();
    if (!response.ok) {
        return fail(responseData.status, { error: JSON.stringify(responseData) });
    }

    redirect(303, `/game/${joincode}`);
};

export const actions = { checkevent, joinevent };
