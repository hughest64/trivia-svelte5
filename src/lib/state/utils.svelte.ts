import { getContext, setContext } from 'svelte';
import { UserState } from './userState.svelte';
import { GameState, type GameStateParams } from './gameState.svelte';
import type { UserData } from '$lib/types';

interface StateTypes {
    userState: UserState;
    gameState: GameState;
}

type ST = UserState | GameState;
type DT = UserData | GameStateParams;

interface DataTypes {
    userState: UserData;
    gameState: GameStateParams;
}

const stateMap = {
    userState: (data: UserData) => new UserState(data),
    gameState: (data: GameStateParams) => new GameState(data)
};

class StateClass {
    static userState(data: UserData) {
        return new UserState(data);
    }
    static gameState(data: GameStateParams) {
        return new GameState(data);
    }
}

export function createState<K extends keyof typeof stateMap>(key: K, data?: any) {
    const stateData = StateClass[key](data) as ReturnType<(typeof stateMap)[K]>;

    return setContext(key, stateData);
}

export function getState<K extends keyof typeof stateMap>(key: K): ReturnType<(typeof stateMap)[K]> {
    return getContext(key);
}
