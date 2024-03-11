import { handleHostAuth } from '$lib/utils';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async (loadEvent) => {
    return handleHostAuth({ ...loadEvent, endPoint: '/user' });
};
