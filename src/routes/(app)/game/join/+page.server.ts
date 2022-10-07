import { invalid, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

const joinevent: Action = async ({ fetch, request }) => {
    const formData = await request.formData();
    const joincode = formData.get('joincode');
    
    if (!joincode) {
        return { errors: { message: 'Please Enter a Join Code' } };
    }
    const response = await fetch(`${apiHost}/game/${joincode}`);

    const responseData = await response.json();
    if (!response.ok) {
        return invalid(responseData.status, { error: responseData.detail });
    }

    throw redirect(303, `/game/${joincode}`);
};

export const actions = { joinevent };
