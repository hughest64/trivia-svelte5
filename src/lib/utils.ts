import type { RequestHandlerOutput } from '@sveltejs/kit';
import * as cookie from 'cookie'

export const getEventCookie = (params: Record<string, string>, request: Request): string => {
    const cookies = cookie.parse(request.headers.get('cookie') || '');
    const eventKey = `event-${params.joincode}`;
    const eventCookie = cookies[eventKey] || '{}';

    return eventCookie;
}

export const setEventCookie = async (
    params: Record<string, string>,
    request: Request
): Promise<RequestHandlerOutput> => {

    const data = await request.json()
    const eventKey = `event-${params.joincode}`;

    return {
        headers: {
            accept: 'application/json',
            'set-cookie': cookie.serialize(eventKey, JSON.stringify(data), {
                path: '/',
                httpOnly: true,
                maxAge: 60 * 60 * 24 // 24 hrs
            })
        }
    }
}