import { getContext, setContext } from 'svelte';
import { UserState } from './userState.svelte';
import { GameState, type GameStateData } from './gameState.svelte';
import type { UserData } from '$lib/types';

function getState<K extends keyof typeof stateManager>(key: K): ReturnType<(typeof stateManager)[K]> {
    return getContext(key);
}
const stateManager = {
    userState: (data?: UserData) => setContext('userState', data && new UserState(data)),
    gameState: (data?: GameStateData) => setContext('gameState', data && new GameState(data)),
    getState
};

export default stateManager;
