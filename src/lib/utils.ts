import { getContext, setContext } from 'svelte';
import { writable, type Writable } from 'svelte/store';
import jwt_decode from 'jwt-decode';
import type { Cookies } from '@sveltejs/kit';
import type { JwtPayload, StoreKey, UserTeam } from './types';

/**
 * take one or many cookie keys and invalidate them by creating new cookies with an exipiration
 * at the beginning of the time epoch
 * @param keys a single cookie key or multiple keys in an array
 * @returns an array of cookies to invalidate (delete)
 */
export const invalidateCookies = (cookies: Cookies, keys: string | string[]): void => {
    if (!Array.isArray(keys)) {
        keys = [keys];
    }
    keys.forEach((key) => {
        cookies.set(key, '', { path: '/', expires: new Date(0) });
    });
};

export function createStore<T>(key: StoreKey, data: T): Writable<T> {
    return setContext(key, writable(data));
}

export function getStore<T>(key: StoreKey): Writable<T> {
    return getContext(key);
}

export const getJwtPayload = (token?: string): JwtPayload => {
    if (!token) return { validtoken: false };

    const payload = jwt_decode<JwtPayload>(token);
    payload.validtoken = Date.now() / 1000 < (payload.exp || NaN);

    return payload;
};

// sort a user's teams so their active team comes first
export const sortUserTeams = (userTeams: UserTeam[], activeTeamId: number): UserTeam[] | void => {
    const activeTeamIndex = userTeams.findIndex((team) => team.id === activeTeamId);
    if (!activeTeamIndex) return;

    const updatedTeams = [...userTeams];
    const activeTeam = updatedTeams.splice(activeTeamIndex, 1)[0];

    return [activeTeam, ...updatedTeams];
};
