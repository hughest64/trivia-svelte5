import { fail } from '@sveltejs/kit';
import { resolveBool } from '$lib/utils';
import { env } from '$env/dynamic/public';
import type { Action } from './$types';

async function asyncTimeout(ms = 100): Promise<ReturnType<typeof setTimeout>> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

const reveal: Action = async ({ fetch, request, params }) => {
    const formData = await request.formData();
    const data = Object.fromEntries(formData.entries());
    const apiHost = env.PUBLIC_API_HOST;
    const requestUrl = `${apiHost}/host/${params.joincode}/reveal`;

    if (!data.update) {
        const revealResponse = await fetch(requestUrl, {
            method: 'post',
            body: JSON.stringify({ ...data, update: false })
        });

        const revealData = await revealResponse.json();
        if (revealData.status && revealData.status !== 200) {
            return fail(revealData.status, { error: revealData.detail });
        }
    }

    // 5 seconds by default on reveal only
    resolveBool(data.reveal as string) && (await asyncTimeout(Number(env.PUBLIC_QUESTION_REVEAL_TIMEOUT)));
    const updateResponse = await fetch(requestUrl, {
        method: 'post',
        body: JSON.stringify({ ...data, update: true })
    });

    const updateData = await updateResponse.json();
    if (updateData.status && updateData.status !== 200) {
        return fail(updateData.status, { error: updateData.detail });
    }

    return { success: true };
};

const lock: Action = async ({ fetch, params, request }) => {
    const formData = await request.formData();
    const data = Object.fromEntries(formData.entries());

    const apiHost = env.PUBLIC_API_HOST;
    const response = await fetch(`${apiHost}/host/${params.joincode}/lock`, {
        method: 'post',
        body: JSON.stringify(data)
    });

    const responseData = await response.json();
    if (responseData.status && responseData.status !== 200) {
        return fail(responseData.status, { error: responseData.detail });
    }

    return { success: true };
};

export const actions = { reveal, lock };
