import { env } from '$env/dynamic/public';
import type { Action } from './$types';

const setmegaround: Action = async ({ fetch, request, url, params }) => {
    console.log('hi there');
    const mr_values = Object.fromEntries(await request.formData());
    const round_number = url.searchParams.get('rd');
    const response = await fetch(`${env.PUBLIC_API_HOST}/game/${params.joincode}/megaround`, {
        method: 'post',
        body: JSON.stringify({ mr_values, round_number })
    });
    console.log(await response.json());
};

export const actions = { setmegaround };
