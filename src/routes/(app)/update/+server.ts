import type { RequestHandler } from './$types';
import { PUBLIC_COOKIE_MAX_AGE } from '$env/static/public';

export const POST: RequestHandler = async ({ cookies, request }) => {
    const { initialRoundNumber, initialQuestionNumber, joincode } = await request.json();

    if (initialRoundNumber && initialQuestionNumber) {
        cookies.set(`event-${joincode}`, JSON.stringify({ initialRoundNumber, initialQuestionNumber }), {
            path: '/',
            httpOnly: true,
            maxAge: Number(PUBLIC_COOKIE_MAX_AGE) || 60 * 60
        });
    }

    return new Response();
};
