import { validateJwt } from '$lib/utils';
import type { Handle, HandleFetch } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    const { cookies, params, request } = event;
    const csrftoken = cookies.get('csrftoken') || '';
    const jwt = cookies.get('jwt') || '';

    event.locals.validtoken = validateJwt(jwt);

    if (jwt && csrftoken) {
        event.locals.fetchHeaders = {
            'content-type': 'application/json',
            cookie: request.headers.get('cookie') || '',
            'x-csrftoken': csrftoken
        };
    }

    const activeData = cookies.get(`event-${params.joincode}`);
    if (activeData) {
        const { activeRoundNumber, activeQuestionNumber } = JSON.parse(activeData);
        event.locals.activeRoundNumber = activeRoundNumber || '';
        event.locals.activeQuestionNumber = activeQuestionNumber || '';
    }
    const response = await resolve(event);

    return response;
};

export const handleFetch: HandleFetch = async ({ event, request }) => {
    const requestMod = new Request(request.url, {
        method: request.method,
        headers: { ...request.headers, ...event.locals.fetchHeaders },
        body: request.body
    });

    return fetch(requestMod);
};
