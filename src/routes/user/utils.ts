import { error } from '@sveltejs/kit';
import { PUBLIC_OAUTH_CALLBACK_URL, PUBLIC_GOOGLE_CLIENT_ID } from '$env/static/public';

// use as the href of an anchor tag to start the google oauth2 process
export const googleAuthUrl = () => {
    const googleAuthParams = new URLSearchParams({
        client_id: PUBLIC_GOOGLE_CLIENT_ID,
        redirect_uri: `${PUBLIC_OAUTH_CALLBACK_URL}`,
        scope: 'email profile',
        response_type: 'code',
        access_type: 'offline'
        // this would force confirmation from the user
        // prompt: 'consent'
    });
    return `https://accounts.google.com/o/oauth2/v2/auth?${googleAuthParams}`;
};

// get an access token from google, note the google client secret must be passed in here
// as this module is not server only and and the secret should not be imported into client code!
export const googleAuthToken = async (code: string, secret: string) => {
    const body = {
        client_id: PUBLIC_GOOGLE_CLIENT_ID,
        client_secret: secret,
        redirect_uri: PUBLIC_OAUTH_CALLBACK_URL,
        grant_type: 'authorization_code',
        code
    };

    const authResp = await fetch('https://oauth2.googleapis.com/token', {
        method: 'post',
        body: JSON.stringify(body)
    });

    if (!authResp.ok) {
        // TODO: perhaps a code here to help us debug where the issue occred?
        throw error(400, { message: 'Cannot authenticate with Google' });
    }

    return authResp.json();
};
