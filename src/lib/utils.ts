import * as cookie from 'cookie'
import type { LoadOutput, RequestHandlerOutput } from '@sveltejs/kit';

// TODO: doc strings for all!

const cookieMaxAge = import.meta.env.VITE_COOKIE_MAX_AGE

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
                maxAge: cookieMaxAge
            })
        }
    }
}

export const setCsrfHeaders = (csrfToken: string): Record<string, string> => {
    return {
        Cookie: `csrftoken=${csrfToken}`,
        'X-CSRFToken': csrfToken
    }
}

export const getFetchConfig = (
    method: string,
    data?: Record<string, unknown>,
    headers?: Record<string, unknown>,
): RequestInit => {
    const requestHeaders: Record<string, unknown> = {
        'content-type': 'application/json',
        accept: 'application/json'
    }
    headers && Object.assign(requestHeaders, headers)

    return {
		method,
        credentials: 'include',
		headers: <HeadersInit>requestHeaders,
		body: data && JSON.stringify(data)
	}
}

export const checkStatusCode = (response: Response, next?: string): LoadOutput => {
    let output: LoadOutput

    switch (response.status) {
        case(500):
            output = { status: 500 }
            break
        case(404):
            output = { status: 404 }
            break
        case(401):
            output = { status: 302, redirect: '/' }
            break
        case(403):
            output = { status: 302, redirect: '/user/login' }
            break
        case(200):
        default:
            output = { status: 200 }
            break

    }
    if (next && output?.redirect && response.status !== 401) {
         output.redirect += `?next=${next}`
    }
    
    return output
}