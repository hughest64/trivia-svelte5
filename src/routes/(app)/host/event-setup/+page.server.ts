// import { invalid } from '@sveltejs/kit';
import type { Action } from './$types';

const fetchEventData: Action = async ({ fetch, request } ) => {
    const data = await request.formData();
    const gameId = data.get('game-select');
    const locationId = data.get('location-select');
    
    const response = await fetch('http://localhost:8000/host/event-setup/',
        {
            method: 'POST',
            // headers: locals.fetchHeaders || {},
            body: JSON.stringify({ gameId, locationId })
        }
    );
    // if !response.ok
    console.log(await response.json());
    // throw invalid (import thing)
    // throw invalid(200, { error: 'Feature Not Implemented' });
    // else redirect to /host/<joincode from response data>
};

export const actions = { fetchEventData };