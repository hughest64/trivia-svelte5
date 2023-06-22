import type { ParamMatcher } from '@sveltejs/kit';
import { getJwtPayload } from '$lib/utils';

export const match: ParamMatcher = (token) => {
    try {
        const payload = getJwtPayload(token);
        console.log(payload);

        return !!payload?.id;
    } catch {
        return false;
    }
};
