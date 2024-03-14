import { getContext, setContext } from 'svelte';
import { UserState } from './userState.svelte';
import { GameState, type GameStateData } from './gameState.svelte';
import type { UserData } from '$lib/types';

// https://stackoverflow.com/questions/64527150/in-typescript-how-to-select-a-type-from-a-union-using-a-literal-type-property

type UserStateParams = {
    type: 'userState';
    input: UserData;
    output: UserState;
};

type GameStateParams = {
    type: 'gameState';
    input: GameStateData;
    output: GameState;
};

type StateOpts = UserStateParams | GameStateParams;

// this results in UserData
type Tizype = Extract<StateOpts, { type: 'userState' }>['input'];

const sm = {
    userState: (data: UserStateParams['input']) => new UserState(data),
    gameState: (data: GameStateParams['input']) => new GameState(data)
};

export function stateSetter(
    key: keyof typeof sm,
    data: Extract<StateOpts, { type: 'userState' }>['input']
): Extract<StateOpts, { type: 'userState' }>['output'] {
    const retData = sm[key](data);
    return retData;
}

////////////////////////////////////////////////////////////////
const stateMap = {
    userState: (data: UserData) => new UserState(data),
    gameState: (data: GameStateData) => new GameState(data)
};

export function createState<K extends keyof typeof stateMap>(key: K, data?: any) {
    const stateData = stateMap[key](data) as ReturnType<(typeof stateMap)[K]>;

    return setContext(key, stateData);
}

export function getState<K extends keyof typeof stateMap>(key: K): ReturnType<(typeof stateMap)[K]> {
    return getContext(key);
}
