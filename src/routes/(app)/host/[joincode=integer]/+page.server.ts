import { invalid } from '@sveltejs/kit';
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
        return invalid(revealResponse.status, { error: revealData.detail });
    }

    // 5 seconds by default on reveal only
    data.value && (await asyncTimeout(Number(updateDelay)));

    const updateResponse = await fetch(`${baseUrl}/update/`, {
        method: 'post',
        body: JSON.stringify(data)
    });

    const updateData = await updateResponse.json();
    if (!updateResponse.ok) {
        return invalid(updateResponse.status, { error: updateData.detail });
    }

    return { success: true };
};

export const actions = { reveal };
