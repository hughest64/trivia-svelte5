import { getContext, setContext } from 'svelte';
import { writable, type Writable } from 'svelte/store';
import jwt_decode from 'jwt-decode';
import type { Cookies } from '@sveltejs/kit';
import type { CurrentEventData, GameQuestion, GameRound, JwtPayload, StoreKey, UserTeam } from './types';

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
    // TODO: shoudl this be if (activeTeamIndex === -1):
    if (!activeTeamIndex) return;

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

export const getCurrentDataFromKey = (key: string): CurrentEventData => {
    const split = key.split('.');

    return {
        round_number: Number(split[0]),
        question_number: Number(split.slice(-1)),
        question_key: key
    };
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
