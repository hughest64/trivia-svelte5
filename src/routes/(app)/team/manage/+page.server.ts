import { fail } from '@sveltejs/kit';
import { PUBLIC_API_HOST } from '$env/static/public';
import type { Actions } from './$types';

export const actions: Actions = {
    updatename: async ({ request, fetch, url }) => {
        const data = Object.fromEntries(await request.formData());
        const prev = url.searchParams.get('prev');
        const joincodereg = /^\/game\/(?<joincode>\d+)\/?/;
        const joincode = prev?.match(joincodereg)?.groups?.joincode;
        Object.assign(data, { joincode });

        const response = await fetch(`${PUBLIC_API_HOST}/team/updateteamname`, {
            method: 'post',
            body: JSON.stringify(data)
        });
        const respData = await response.json();
        if (!response.ok) {
            return fail(response.status, { error: { teamname: respData.detail } });
        }

        return { success: { teamname: respData.detail } };
    },
    'remove-team-members': async ({ request, fetch, url }) => {
        const data = Object.keys(Object.fromEntries(await request.formData()));
        const team_id = url.searchParams.get('team_id');
        const payload = { usernames: data, team_id };

        const response = await fetch(`${PUBLIC_API_HOST}/team/remove-team-members`, {
            method: 'post',
            body: JSON.stringify(payload)
        });
        const respdata = await response.json();
        if (!response.ok) {
            return fail(response.status, { error: { teampassword: respdata.detail } });
        }

        return { success: { teampassword: respdata.detail } };
    },
    'update-password': async ({ request, fetch, url }) => {
        const data = Object.fromEntries(await request.formData());
        const prev = url.searchParams.get('prev');
        const joincodereg = /^\/game\/(?<joincode>\d+)\/?/;
        const joincode = prev?.match(joincodereg)?.groups?.joincode;
        Object.assign(data, { joincode });

        const response = await fetch(`${PUBLIC_API_HOST}/team/update-password`, {
            method: 'post',
            body: JSON.stringify(data)
        });

        const respData = await response.json();
        if (!response.ok) {
            return fail(response.status, { error: { password: respData.detail } });
        }

        return { success: { password: respData.detail } };
    }
};
