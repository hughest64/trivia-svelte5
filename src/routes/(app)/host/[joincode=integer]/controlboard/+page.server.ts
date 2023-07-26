import { PUBLIC_API_HOST } from '$env/static/public';

export const load = async ({ locals, params, url, fetch }) => {
    let apiData = {};

    const response = await fetch(`${PUBLIC_API_HOST}/host/${params.joincode}/tiebreaker`);
    if (response.ok) {
        apiData = await response.json();
    } else {
        // TODO: throw error
    }

    return { ...locals, ...apiData };
};
