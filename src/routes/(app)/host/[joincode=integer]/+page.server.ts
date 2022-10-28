import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { Action } from './$types';

async function asyncTimeout(ms=100): Promise<ReturnType<typeof setTimeout>> {
    return new Promise((resolve) => setTimeout(resolve, ms));
};

const reveal: Action = async ({ fetch, request, params }) => {
    const formData = await request.formData();
    const data = Object.fromEntries(formData.entries());

    // notify players (no db update)
    const revealResponse = await fetch(`${apiHost}/host/${params.joincode}/reveal/`, {
        method: 'post',
        body: JSON.stringify(data)
    });
    
    await asyncTimeout(5000);
    // update the db
    const updateResponse = await fetch(`${apiHost}/host/${params.joincode}/update/`, {
        method: 'post',
        body: JSON.stringify({ data: 'lock the round' })
    });
    const updateData = await updateResponse.json();
    
    const revealData = await revealResponse.json();
    return { revealData, updateData };
};

export const actions = { reveal };
