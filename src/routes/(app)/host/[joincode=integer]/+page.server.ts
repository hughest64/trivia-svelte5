import type { Action } from './$types';

const reveal: Action = async ({ request }) => {
    const data = await request.formData();
    console.log('data', data.get('value'));

    // for the case of a single question key will be r.q
    // for the case of revealAll the key will be 'all'
    const key = data.get('key');
    console.log('key', key);

    // post the message that a q will be revealed (no db update)
    // async timeout
    // post the db update

    // will this return before the timeout completes?
    return { success: true };
};

export const actions = { reveal };