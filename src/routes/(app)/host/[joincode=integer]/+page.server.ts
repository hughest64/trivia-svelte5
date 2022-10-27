import type { Action } from './$types';

const reveal: Action = async ({ request, url }) => {
    console.log('hello');
    const data = Object.fromEntries((await request.formData()).entries());
    console.log(data);
};

export const actions = {
    reveal
};