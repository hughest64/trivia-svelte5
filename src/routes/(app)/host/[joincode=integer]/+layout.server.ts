import { handleHostAuth } from '$lib/utils';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async (loadEvent) => {
    // TODO: consider getting the pathname from new URL(loadEvent.request.url).pathname
    // if we don't want to hit the api on footer links host side (right now it's requried
    // as we don't load data for scoring when the quiz page is loaded, etc.)
    return handleHostAuth({ ...loadEvent, endPoint: loadEvent.url.pathname });
};
