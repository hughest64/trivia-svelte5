import { fail, redirect } from '@sveltejs/kit';
import { handlePlayerAuth } from '$lib/utils';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action, PageServerLoad } from './$types';

export const load: PageServerLoad = async (loadEvent) => {
    return handlePlayerAuth({ ...loadEvent, endPoint: '/user' });
};

const joinevent: Action = async ({ fetch, request }) => {
    const formData = await request.formData();
    const joincode = formData.get('joincode');

    if (!joincode) {
        return { errors: { message: 'Please Enter a Join Code' } };
    }
    const response = await fetch(`${apiHost}/game/join`, {
        method: 'post',
        body: JSON.stringify({ joincode: joincode })
    });
    const responseData = await response.json();
    if (!response.ok) {
        return fail(responseData.status, { error: responseData.detail });
    }

    throw redirect(303, `/game/${joincode}`);
};

export const actions = { joinevent };
