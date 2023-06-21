import type { ParamMatcher } from '@sveltejs/kit';
import { getJwtPayload } from '$lib/utils';

export const match: ParamMatcher = (token) => {
    const payload = getJwtPayload(token);

    return payload.validtoken || false;
};
