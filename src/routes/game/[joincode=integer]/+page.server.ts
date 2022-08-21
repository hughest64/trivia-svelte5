import * as cookie from 'cookie';
import type { PageServerLoad } from './$types';
import { PUBLIC_COOKIE_MAX_AGE } from '$env/static/public';

export const POST: PageServerLoad = async ({ setHeaders, params, request }) => {
    const { initialRoundNumber, initialQuestionNumber } = await request.json();

    if (initialRoundNumber &&  initialQuestionNumber) {
        setHeaders({
            'set-cookie': cookie.serialize(
                `event-${params.joincode}`,
                JSON.stringify({ initialRoundNumber, initialQuestionNumber }),
                {
                    path: '/',
                    httpOnly: true,
                    maxAge: Number(PUBLIC_COOKIE_MAX_AGE) || 60 * 60
                }
            )
        });
    }
};
