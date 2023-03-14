import { handleHostAuth } from '$lib/utils';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async (loadEvent) => {
    const path = new URL(loadEvent.request.url).pathname.split('/__data.json')[0];
    return handleHostAuth({ ...loadEvent, endPoint: path });
};
