import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

async function asyncTimeout(ms=100): Promise<ReturnType<typeof setTimeout>> {
    return new Promise((resolve) => setTimeout(resolve, ms));
};

const reveal: Action = async ({ fetch, request, params }) => {
    const formData = await request.formData();
    const data = Object.fromEntries(formData.entries());

    const revealResponse = await fetch(`${apiHost}/host/${params.joincode}/reveal/`, {
        method: 'post',
        body: JSON.stringify(data)
    });

    const revealData = await revealResponse.json();
    return revealData;
};

const update: Action = async ({ fetch, request, params }) => {
    const formData = await request.formData();
    const data = Object.fromEntries(formData.entries());
    await asyncTimeout(5000);

    const updateResponse = await fetch(`${apiHost}/host/${params.joincode}/update/`, {
        method: 'post',
        body: JSON.stringify(data)
    });
    const updateData = await updateResponse.json();
    return updateData;
};

export const actions = { reveal, update };
