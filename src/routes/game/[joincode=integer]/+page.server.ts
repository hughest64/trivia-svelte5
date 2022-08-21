import { get as getStore } from 'svelte/store';
import { currentQuestionNumber, currentRoundNumber } from '$stores/event';
import type { PageServerLoad } from './$types';
import { getEventCookie, setEventCookie } from '$lib/utils';

// TODO: just try to read the cookie and return the cookie data
// no worries about current question/round, handle that in page.svelte
export const load: PageServerLoad = async ({ params, request }) => {
    // just use params.joincode to look up the cookie and return
    // initialQuestionNumber initialRoundNumber
    const body = {
        initialRoundNumber: getStore(currentRoundNumber) || 1,
        initialQuestionNumber: getStore(currentQuestionNumber) || 1
    };
    const cookieData = JSON.parse(getEventCookie(params, request));

    return { ...body, ...cookieData };
};

export const POST: PageServerLoad = async ({ /** setHeaders, */ params, request }) => {
    // const formData = await request.formData();
    // get the q and r
    // make the cookie
    // setHeders({ 'set-cookie': 'cookie-string' });
    return await setEventCookie(params, request);
};
