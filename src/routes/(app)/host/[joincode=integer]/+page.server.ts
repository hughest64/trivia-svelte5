import { fail } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost, PUBLIC_QUESTION_REVEAL_TIMEOUT as updateDelay } from '$env/static/public';
import type { Action } from './$types';

async function asyncTimeout(ms = 100): Promise<ReturnType<typeof setTimeout>> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

const reveal: Action = async ({ fetch, request, params }) => {
    const formData = await request.formData();
    const data = Object.fromEntries(formData.entries());
    const baseUrl = `${apiHost}/host/${params.joincode}`;

    const revealResponse = await fetch(`${baseUrl}/reveal/`, {
        method: 'post',
        body: JSON.stringify(data)
    });

    if (!revealResponse.ok) {
        const revealData = await revealResponse.json();
        return fail(revealResponse.status, { error: revealData.detail });
    }

    // 5 seconds by default on reveal only
    data.value && (await asyncTimeout(Number(updateDelay)));
    const revealAll = String(data.key).endsWith('all');

    const updateUrl = revealAll ? `${baseUrl}/update-all/` : `${baseUrl}/update/`;
    const updateResponse = await fetch(updateUrl, {
        method: 'post',
        body: JSON.stringify(data)
    });

    const updateData = await updateResponse.json();
    if (!updateResponse.ok) {
        return fail(updateResponse.status, { error: updateData.detail });
    }

    return { success: true };
};

const lock: Action = async ({ fetch, params, request }) => {
    const formData = await request.formData();
    const data = Object.fromEntries(formData.entries());

    const response = await fetch(`${apiHost}/host/${params.joincode}/lock`, {
        method: 'post',
        body: JSON.stringify(data)
    });

    const responseData = await response.json();
    if (!response.ok) {
        return fail(response.status, { error: responseData.detail });
    }

    return { success: true };
};

export const actions = { reveal, lock };
