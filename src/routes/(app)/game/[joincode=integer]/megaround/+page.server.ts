import { PUBLIC_API_HOST } from '$env/static/public';
import type { Action } from './$types';

const setmegaround: Action = async ({ fetch, request, url, params }) => {
    const mr_values = Object.fromEntries(await request.formData());
    const round_number = url.searchParams.get('rd');
    // TODO: handle the response
    const response = await fetch(`${PUBLIC_API_HOST}/game/${params.joincode}/megaround`, {
        method: 'post',
        body: JSON.stringify({ mr_values, round_number })
    });
    console.log(await response.json());
};

export const actions = { setmegaround };
