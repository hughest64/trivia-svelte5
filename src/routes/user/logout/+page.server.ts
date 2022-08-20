import * as cookie from 'cookie';
// import { getFetchConfig } from '$lib/utils';
// import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import type { PageServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ request, setHeaders }) => {
    // TODO: we can streamline this, eh?
    request.headers.delete('cookie');
    const jwt = cookie.serialize('jwt', '', { path: '/', expires: new Date(0) });
    const csrf = cookie.serialize('csrftoken', '', { path: '/', expires: new Date(0) });
    request.headers.set('csrf', csrf);
    setHeaders({ 'set-cookie': [jwt, csrf] });

    // TODO: we probably only need to do this if we want to delete a token from the db
    // (not that we currently store that information)
    // const fetchConfig = getFetchConfig('POST');
    // const response = await fetch(`${apiHost}/user/logout/` );
    // if (response.ok) {
    //     console.log('ok');
    // }
    throw redirect(302, '/user/login');
};
