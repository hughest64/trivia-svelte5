import { getContext, setContext } from 'svelte';
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

export interface UserData {
    id: number;
    username: string;
    is_staff: boolean;
    email?: string;
    active_team_id?: number | null;
    active_team?: UserTeam | undefined;
    teams: UserTeam[];
    user_is_anonymous?: boolean;
    user_home_locations?: string[];
}

export interface UserTeam {
    id: string | number;
    name: string;
    password: string;
    members?: string[];
}

// TODO: if we keep this, it goes in a different file
enum StoreKeys {
    userData = 'userData'
}

export const setUserActiveTeam = (userData: UserData) => (
    userData.active_team = userData.teams.find((team) => team.id === userData.active_team_id)
);

export const createUserStore = (userData: UserData): void => {
    // find the active team based on id and add it to the userdata
    userData && setUserActiveTeam(userData);
    setContext(StoreKeys.userData, writable(userData));
};

export const getUserStore = (): Writable<UserData> => {
    return getContext(StoreKeys.userData);
};


// testing out typing styles for generic store functions

// Can this be tied to an enum or something similar?
type StoreKey = 'userData' | 'eventData'

interface EventData {
    win: boolean
}

export function createStore<T>(key: StoreKey, data: T): Writable<T> {
    return setContext(key, writable(data));
};

export function getStore<T>(key: StoreKey): Writable<T> {
    return getContext(key);
}

export const user = createStore<EventData>('eventData', { win: true });
export const myUser = getStore<UserData>('userData');
