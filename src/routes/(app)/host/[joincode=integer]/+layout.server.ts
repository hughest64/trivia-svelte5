import { handleHostAuth } from '$lib/utils';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async (loadEvent) => {
    const joincode = loadEvent.params.joincode;
    return handleHostAuth({ ...loadEvent, endPoint: `/host/${joincode}` });
};
