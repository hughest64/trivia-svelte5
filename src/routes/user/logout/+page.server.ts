import { invalidateCookies } from '$lib/utils';
import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

// TODO: this may work better as a single server.ts file rather than page.server and page.svelte
// process the same as here, but return a response object with a status of 302 and a location header

// NOTE: as of now we don't need to send a request to the api as we are controling
// the headers SvelteKit side
export const load: PageServerLoad = async ({ setHeaders }) => {
    // delete auth cookies and redirect
    const invalidatedCookies = invalidateCookies(['jwt', 'csrftoken']);
    setHeaders({ 'set-cookie': invalidatedCookies });
    throw redirect(302, '/welcome');
};
