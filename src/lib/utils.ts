import * as cookie from 'cookie';
import { error, redirect } from '@sveltejs/kit';
import { PUBLIC_API_HOST, PUBLIC_COOKIE_MAX_AGE } from '$env/static/public';
import { getContext, setContext } from 'svelte';
import jwt_decode from 'jwt-decode';
import type { Cookies } from '@sveltejs/kit';
import type {
    ActiveEventData,
    CustomLoadEvent,
    ChatMessage,
    GameQuestion,
    GameRound,
    JwtPayload,
    Response,
    RoundState,
    StoreTypes,
    UserTeam,
    ResponseMeta
} from './types';

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

export function createStore<K extends keyof StoreTypes>(key: K, store: StoreTypes[K]): StoreTypes[K] {
    return setContext(key, store);
}

export function getStore<K extends keyof StoreTypes>(key: K): StoreTypes[K] {
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

// use javascript to set a cookie that tracks the round and question a user is currently viewing
export const setEventCookie = (data: ActiveEventData, joincode: string) => {
    try {
        const cook = cookie.serialize(`event-${joincode}`, JSON.stringify(data), {
            path: '/',
            httpOnly: false,
            maxAge: Number(PUBLIC_COOKIE_MAX_AGE) || 3600,
            sameSite: 'lax'
        });

        document.cookie = cook;

        return cook;
    } catch (e) {
        console.error('could not set event cookie', e);
    }
};

/**
 * filter and back fill missing responses based on round data
 */
export const respsByround = (
    resps: Response[],
    rounds: GameRound[],
    roundStates: RoundState[],
    isHost: boolean = false
) => {
    const roundResps: Record<string, ResponseMeta[]> = {};

    rounds.forEach((rd) => {
        const rdNum = rd.round_number;
        const rdState = roundStates.find((rs) => rs.round_number === rdNum);

        const rdResps = resps.filter((r) => r.round_number === rdNum) || [];
        for (let i = 1; i < rd.question_count + 1; i++) {
            const existingResp = rdResps.find((r) => r.question_number === i);
            const answer = existingResp?.recorded_answer;

            let pts: string | number = '-';
            if (existingResp && (rdState?.scored || (isHost && rdState?.locked))) {
                pts = String(existingResp.points_awarded);
            }

            const resp = {
                key: `${rdNum}.${i}`,
                recorded_answer: answer ? answer : '-',
                points_awarded: pts
            };

            rdNum in roundResps ? roundResps[rdNum].push(resp) : (roundResps[rdNum] = [resp]);
        }
    });

    return Object.values(roundResps);
};

export const groupChats = (chats: ChatMessage[], hostPage: boolean) => {
    if (!chats || chats.length === 0) return [];
    if (chats.length === 1 || hostPage) return chats;

    const groupedChats: ChatMessage[] = [{ ...chats[0] }];
    for (let i = 1; i < chats.length; i++) {
        const chat = chats[i];
        const prevChat = chats[i - 1];

        if (!prevChat.is_host_message && chat.is_host_message) {
            groupedChats.push({ ...chat });
        } else if (chat.userid !== prevChat?.userid) {
            groupedChats.push({ ...chat });
        } else if (prevChat.is_host_message && !chat.is_host_message) {
            groupedChats.push({ ...chat });
        } else {
            const lastGroupedChat = groupedChats[groupedChats.length - 1];
            lastGroupedChat.chat_message += '\n' + chat.chat_message;
            lastGroupedChat.time = chat.time;
        }
    }
    return groupedChats;
};

/**
 * Custom load functions to help keep trivia event endpoints dry. Player
 * and Host routes are handled separately as the logic differs a bit.
 */

const apiMap = new Map([
    ['/host/choice', '/user'],
    ['/game/join', '/user']
]);

export const handlePlayerAuth = async ({
    locals,
    fetch,
    isDataRequest,
    url,
    endPoint
}: CustomLoadEvent): Promise<App.PageData> => {
    const searchParams = new URLSearchParams(url.searchParams);
    if (!locals.validtoken) {
        searchParams.set('next', url.pathname);
        redirect(302, `/user/logout?${decodeURIComponent(searchParams.toString())}`);
    }

    let data = {};
    if (!isDataRequest) {
        const apiEndpoint = apiMap.get(endPoint || '') || endPoint;
        const apiHost = PUBLIC_API_HOST;
        const response = await fetch(`${apiHost}${apiEndpoint}${url.search}`);

        const apiData = await response.json();
        if (response.ok) data = { ...apiData, ...locals };

        // not authorized, redirect to log out to ensure cookies get deleted
        if (response.status === 401) {
            searchParams.set('next', url.pathname);
            redirect(302, `/user/logout?${decodeURIComponent(searchParams.toString())}`);
        }
        // forbidden, redirect to a safe page
        if (response.status === 403) {
            // TODO: add a payload key to the error and send userdata through
            if (apiData?.reason === 'player_limit_exceeded') {
                error(403, { message: apiData.detail, code: apiData.reason });
            }
            redirect(302, `/team${decodeURIComponent(url.search)}`);
        }
        // TODO: expand to handle other pages (/team, etc)
        // resolve the error page
        if (response.status === 404) {
            error(404, { message: apiData.detail, next: '/game/join' });
        }
    }

    return data;
};

export const handleHostAuth = async ({
    locals,
    fetch,
    url,
    endPoint,
    isDataRequest
}: CustomLoadEvent): Promise<App.PageData> => {
    const apiEndpoint = apiMap.get(endPoint || '') || endPoint;

    const searchParams = new URLSearchParams(url.searchParams);

    if (!locals.validtoken) {
        searchParams.set('next', url.pathname);
        redirect(302, `/user/logout?${decodeURIComponent(searchParams.toString())}`);
    }
    if (!locals.staffuser) redirect(302, `/team${decodeURIComponent(url.search)}`);

    let data = {};
    if (!isDataRequest) {
        const apiHost = PUBLIC_API_HOST;
        const response = await fetch(`${apiHost}${apiEndpoint}`);
        const apiData = await response.json();
        if (response.ok) {
            data = { ...apiData, ...locals };
        }
        // not authorized, redirect to log out to ensure cookies get deleted
        if (response.status === 401) {
            searchParams.set('next', url.pathname);
            redirect(302, `/user/logout${decodeURIComponent(searchParams.toString())}`);
        }

        // forbidden, redirect to a safe page
        if (response.status === 403) {
            redirect(302, '/host/choice');
        }

        if (response.status === 404) {
            error(404, { message: apiData.detail, next: '/host/choice' });
        }
    }

    return data;
};
