import type { Action } from './$types';

const setmegaround: Action = async ({ fetch, request }) => {
    const values = Object.fromEntries(await request.formData());
    console.log(values);
};

export const actions = { setmegaround };
