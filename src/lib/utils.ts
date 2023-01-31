import { error, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST as apiHost } from '$env/static/public';
import { getContext, setContext } from 'svelte';
import { writable, type Writable } from 'svelte/store';
import jwt_decode from 'jwt-decode';
import type { Cookies } from '@sveltejs/kit';
import type { CustomLoadEvent, GameQuestion, GameRound, JwtPayload, StoreKey, UserTeam } from './types';

/**
 * take one or many cookie keys and invalidate them by creating new cookies with an exipiration
 * at the beginning of the time epoch
 * @param keys a single cookie key or multiple keys in an array
 * @returns an array of cookies to invalidate (delete)
 */
export const invalidateCookies = (cookies: Cookies, keys: string | string[]): void => {
    const allKeys = !Array.isArray(keys) ? [keys] : keys;
    allKeys.forEach((key) => {
        cookies.set(key, '', { path: '/', httpOnly: true, secure: false, expires: new Date(0) });
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
    if (activeTeamIndex === -1) return;

    const updatedTeams = [...userTeams];
    const activeTeam = updatedTeams.splice(activeTeamIndex, 1)[0];

    return [activeTeam, ...updatedTeams];
};

interface RoundQuestion {
    round: string;
    question: string;
}
/**
 * uses simple regex to split a question key into an object
 * @param key a string of roundnumber.questionnumber like 1.1
 * @returns an object containing the round and question numbers as strings
 */
export const splitQuestionKey = (key: string): RoundQuestion => {
    const keyReg = /^(?<r>\d+).(?<q>\d+)$/;
    const groups = key.match(keyReg)?.groups;
    return { round: groups?.r || '', question: groups?.q || '' };
};

export const createQuestionKey = (roundNumber: number, questionNumber: number): string => {
    return `${roundNumber}.${questionNumber}`;
};

export const getQuestionKeys = (questions: GameQuestion[], activeRound: GameRound): string[] => {
    const keys = [];
    for (const q of questions) {
        if (q.round_number === activeRound.round_number) {
            keys.push(q.key);
        }
    }
    return keys;
};

export const resolveBool = (value: string | boolean) => {
    if (value === 'false') return false;
    return Boolean(value);
};

/**
 * Custom load functions to help keep trivia event endpoints dry. Player
 * and Host routes are handled separately as the logic differs a bit.
 */

const apiMap = new Map([
    ['/host/choice', '/user'],
    ['/game/join', '/user']
]);

export const handlePlayerAuth = async ({ locals, fetch, url, endPoint }: CustomLoadEvent): Promise<App.PageData> => {
    if (!locals.validtoken) throw redirect(302, `/user/logout?next=${url.pathname}`);

    const apiEndpoint = apiMap.get(endPoint || '') || endPoint;
    const response = await fetch(`${apiHost}${apiEndpoint}/`);

    let data = {};
    const apiData = await response.json();
    if (response.ok) data = { ...apiData, ...locals };

    // not authorized, redirect to log out to ensure cookies get deleted
    if (response.status === 401) {
        throw redirect(302, `/user/logout?next=${url.pathname}`);
    }
    // forbidden, redirect to a safe page
    if (response.status === 403) {
        if (apiData?.reason === 'join_required') {
            // TODO: auto-join, i.e. post to /game/join w/ params.joincode
            // if ok, return data, else redirect or error accordingly
            throw redirect(302, `/game/join?reason=${apiData.reason}`);
        }
        throw redirect(302, '/team');
    }
    // TODO: expand to handle other pages (/team, etc)
    // resolve the error page
    if (response.status === 404) {
        throw error(404, { message: apiData.detail, next: '/game/join' });
    }

    return data;
};

export const handleHostAuth = async ({ locals, fetch, url, endPoint }: CustomLoadEvent): Promise<App.PageData> => {
    const apiEndpoint = apiMap.get(endPoint || '') || endPoint;

    if (!locals.validtoken) throw redirect(302, `/user/logout?next=${url.pathname}`);
    if (!locals.staffuser) throw redirect(302, '/team');

    const response = await fetch(`${apiHost}${apiEndpoint}/`);

    let data = {};
    const apiData = await response.json();
    if (response.ok) {
        data = { ...apiData, ...locals };
    }

    // not authorized, redirect to log out to ensure cookies get deleted
    if (response.status === 401) {
        throw redirect(302, `/user/logout?next=${url.pathname}`);
    }

    // forbidden, redirect to a safe page
    if (response.status === 403) {
        throw redirect(302, '/host/choice');
    }

    if (response.status === 404) {
        throw error(404, { message: apiData.detail, next: '/host/choice' });
    }

    return data;
};
