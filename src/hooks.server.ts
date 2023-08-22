import { getJwtPayload } from '$lib/utils';
import { PUBLIC_WEBSOCKET_HOST, PUBLIC_QUESTION_REVEAL_TIMEOUT } from '$env/static/public';
import type { Handle, HandleFetch } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
    const { cookies, params, request } = event;
    const csrftoken = cookies.get('csrftoken') || '';
    const jwt = cookies.get('jwt') || '';

    if (jwt && csrftoken) {
        const jwtPayload = getJwtPayload(jwt);
        event.locals.validtoken = jwtPayload.validtoken;
        event.locals.staffuser = jwtPayload.staff_user;
        event.locals.jwt = jwt;

        event.locals.fetchHeaders = {
            'content-type': 'application/json',
            cookie: request.headers.get('cookie') || '',
            'x-csrftoken': csrftoken
        };
    }

    const activeData = cookies.get(`event-${params.joincode}`);
    if (activeData) {
        const { activeRoundNumber, activeQuestionNumber, activeQuestionKey } = JSON.parse(activeData);
        event.locals.activeRoundNumber = activeRoundNumber || '';
        event.locals.activeQuestionNumber = activeQuestionNumber || '';
        event.locals.activeQuestionKey = activeQuestionKey || '';
    }
    event.locals.websocketHost = PUBLIC_WEBSOCKET_HOST;
    event.locals.updateDelay = Number(PUBLIC_QUESTION_REVEAL_TIMEOUT);

    const response = await resolve(event);
    return response;
};

export const handleFetch: HandleFetch = async ({ event, request }) => {
    try {
        for (const [key, value] of Object.entries(<Record<string, string>>event.locals.fetchHeaders)) {
            request.headers.set(key, value);
        }
    } catch (e) {
        // console.error(e);
    }

    return fetch(request);
};
