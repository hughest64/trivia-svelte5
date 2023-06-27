import { env } from '$env/dynamic/public';
import { redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET = (async ({ fetch, url }) => {
    const code = url.searchParams.get('code');
    // TODO: handle if we don't have a code
    const body = {
        client_id: env.PUBLIC_GOOGLE_CLIENT_ID,
        client_secret: env.PUBLIC_GOOGLE_CLIENT_SECRET,
        redirect_uri: 'http://127.0.0.1:5173/user/google-auth',
        grant_type: 'authorization_code',
        code
    };

    const authResp = await fetch('https://oauth2.googleapis.com/token', {
        method: 'post',
        body: JSON.stringify(body)
    });
    // TODO: handle errors here
    const authData = await authResp.json();

    // TODO: go to the api and have django get the actual user data
    const userResp = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
        headers: { Authorization: `Bearer ${authData.access_token}` }
    });
    const userData = await userResp.json();
    console.log(userData);

    // get the jwt and set the cookie
    // use getJwtPayload to determine it's a host or player then
    // redirect to /team, or /host/choice
    throw redirect(302, '/');
}) satisfies RequestHandler;
