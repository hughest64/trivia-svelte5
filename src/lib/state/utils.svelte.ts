import { getContext, setContext } from 'svelte';
import { UserState } from './userState.svelte';
import type { UserData } from '$lib/types';

const stateMap = {
    userState: (data?: UserData) => data && new UserState(data)
};

interface StateTypes {
    userState?: UserState;
}

interface DataTypes {
    userState?: UserData;
}

export function createState<K extends keyof typeof stateMap>(key: K, data: DataTypes[K]): StateTypes[K] {
    return setContext(key, stateMap[key](data));
}

export function getState<K extends keyof typeof stateMap>(key: K): StateTypes[K] {
    return getContext(key);
}
