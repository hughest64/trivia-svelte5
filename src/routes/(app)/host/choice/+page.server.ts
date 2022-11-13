import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals }) => {
    // prevent players from accessing this host only endpoint
    if (!locals.staffuser) throw redirect(302, '/team');
};
