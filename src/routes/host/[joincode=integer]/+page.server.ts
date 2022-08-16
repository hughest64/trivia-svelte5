import { get as getStore } from 'svelte/store';
import { currentQuestionNumber, currentRoundNumber } from '$stores/event';
import type { PageServerLoad } from './$types';
import { getEventCookie, setEventCookie } from '$lib/utils';

export const load: PageServerLoad = async ({ params, request }) => {
    const body = {
        initialRoundNumber: getStore(currentRoundNumber) || 1,
        initialQuestionNumber: getStore(currentQuestionNumber) || 1
    };
    const cookieData = JSON.parse(getEventCookie(params, request));

    return {
        data: { ...body, ...cookieData }
    };
};

export const POST: PageServerLoad = async ({ params, request }) => {
    return await setEventCookie(params, request);
};
