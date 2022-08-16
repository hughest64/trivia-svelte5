import { get as getStore } from 'svelte/store';
import { currentQuestionNumber, currentRoundNumber } from '$stores/event';
import type { PageServerLoad, Action } from '@sveltejs/kit';
import { getEventCookie, setEventCookie } from '$lib/utils';

export const load: PageServerLoad = async ({ params, request }) => {
    const body = {
        initialRoundNumber: getStore(currentRoundNumber) || 1,
        initialQuestionNumber: getStore(currentQuestionNumber) || 1
    };
    const cookieData = JSON.parse(getEventCookie(params, request));

    throw new Error("@migration task: Migrate this return statement (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292699)");
    return {
        headers: { accept: 'application/json' },
        body: { ...body, ...cookieData }
    };
};

export const POST: Action = async ({ params, request }) => {
    throw new Error("@migration task: Migrate this return statement (https://github.com/sveltejs/kit/discussions/5774#discussioncomment-3292699)");
    return await setEventCookie(params, request);
};
