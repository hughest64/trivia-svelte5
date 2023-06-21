import type { ParamMatcher } from '@sveltejs/kit';

export const match: ParamMatcher = (param) => {
    // TODO: use jwtdecode to ensure it's a valid token
    return true;
};
