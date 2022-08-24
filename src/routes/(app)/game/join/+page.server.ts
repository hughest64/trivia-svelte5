import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

export const POST: Action = async ({ locals, request }) => {
    const formData = await request.formData();
    const joincode = formData.get('joincode');
    
    if (!joincode) {
        return { errors: { message: 'Please Enter a Join Code' } };
    }
    const response = await fetch(`${apiHost}/event/${joincode}`,
        {
            method: 'GET',
            headers: locals.fetchHeaders
        }
    );
    const responseData = await response.json();
    if (!response.ok) {
        return { errors: { message: responseData.detail } };
    }

    return { location: `/game/${joincode}` };

};
