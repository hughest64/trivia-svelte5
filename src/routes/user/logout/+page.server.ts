import { invalidateCookies } from '$lib/utils';
import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ setHeaders }) => {
    // delete auth cookies and redirect
    const invalidatedCookies = invalidateCookies(['jwt', 'csrftoken']);
    setHeaders({ 'set-cookie': invalidatedCookies });

    throw redirect(302, '/');
};
