import { PUBLIC_API_HOST } from '$env/static/public';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
    const response = await fetch(`${PUBLIC_API_HOST}/changelog`);
    const apiData = await response.json();
    if (!response.ok) {
        console.error(apiData);
        return { error: 'An error occurred' };
    }
    return apiData;
};
