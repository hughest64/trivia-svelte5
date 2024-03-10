import type { LayoutServerLoad } from './$types';
import { PUBLIC_API_HOST } from '$env/static/public';

export const load: LayoutServerLoad = async ({ fetch, params }) => {
    const resp = await fetch(`${PUBLIC_API_HOST}/host/${params.joincode}`);
    const respData = await resp.json();

    return respData;
};
