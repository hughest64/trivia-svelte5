
import { get as getStore } from 'svelte/store'
import * as cookie from 'cookie'
import { currentQuestionNumber, currentRoundNumber } from '$stores/event';
import type { RequestHandler } from '@sveltejs/kit';

export const get: RequestHandler = async ({ params, request }) => {
    const cookies = cookie.parse(request.headers.get('cookie') || '');
    const eventKey = `event-${params.joincode}`;
    const eventCookie = cookies[eventKey]
    const body = {
        initialRoundNumber: getStore(currentRoundNumber) || 1,
        initialQuestionNumber: getStore(currentQuestionNumber) || 1
    }
    eventCookie && Object.assign(body, JSON.parse(eventCookie))
    
    return {
        headers: { accept: 'application/json' },
        body
    }
}

export const post: RequestHandler = async ({ params, request }) => {
    const data = await request.json()
    const eventKey = `event-${params.joincode}`;

    return {
        headers: {
            accept: 'application/json',
            'set-cookie': cookie.serialize(eventKey, JSON.stringify(data), {
                path: '/',
                httpOnly: true
            })
        }
    }
}