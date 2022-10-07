import { invalid, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

const fetchEventData: Action = async ({ fetch, request }) => {
    const data = await request.formData();
    const gameId = data.get('game-select');
    const locationId = data.get('location-select');

    const response = await fetch(`${apiHost}/host/event-setup/`, {
        method: 'POST',
        body: JSON.stringify({ gameId, locationId })
    });

    const responseData = await response.json();
    if (!response.ok) {
        return invalid(response.status, { error: responseData.detail });
    }
    
    const joinCode = responseData?.event_data?.join_code;
    throw redirect(302, `/host/${joinCode}`);
};

export const actions = { fetchEventData };
