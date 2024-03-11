import { invalidateCookies } from '$lib/utils';
import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ cookies, url }) => {
    // delete auth cookies and redirect
    invalidateCookies(cookies, ['jwt', 'csrftoken']);

    redirect(302, `/${url.search}`);
};
