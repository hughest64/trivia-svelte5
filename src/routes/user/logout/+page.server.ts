import { invalidateCookies } from '$lib/utils';
import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ cookies, url }) => {
    // delete auth cookies and redirect
    invalidateCookies(cookies, ['jwt', 'csrftoken']);

    const next = url.searchParams.get('next');
    const path = next ? `/?next=${next}` : '/';

    throw redirect(302, path);
};
