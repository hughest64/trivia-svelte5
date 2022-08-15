import { get as getStore } from 'svelte/store';
import { currentQuestionNumber, currentRoundNumber } from '$stores/event';
import type { RequestHandler } from '@sveltejs/kit';
import { getEventCookie, setEventCookie } from '$lib/utils';

export const GET: RequestHandler = async ({ params, request }) => {
    const body = {
        initialRoundNumber: getStore(currentRoundNumber) || 1,
        initialQuestionNumber: getStore(currentQuestionNumber) || 1
    };
    const cookieData = JSON.parse(getEventCookie(params, request));

    return {
        headers: { accept: 'application/json' },
        body: { ...body, ...cookieData }
    };
};

export const POST: RequestHandler = async ({ params, request }) => {
    return await setEventCookie(params, request);
};
