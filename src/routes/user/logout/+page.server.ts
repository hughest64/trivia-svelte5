import { invalidateCookies } from '$lib/utils';
import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ cookies }) => {
    // delete auth cookies and redirect
    invalidateCookies(cookies, ['jwt', 'csrftoken']);

    throw redirect(302, '/');
};
