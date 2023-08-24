import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

// not content at /host, redirect to /host/choice
export const load: PageServerLoad = ({ url }) => {
    if (url.pathname.match(/host\/?$/)) {
        throw redirect(302, '/host/choice');
    }
};
