import { getContext, setContext } from 'svelte';
import { UserState } from './userState.svelte';
import { EventHandler } from './eventHandler.svelte';
import type { UserData } from '$lib/types';

export function getState<K extends keyof typeof createState>(key: K): ReturnType<(typeof createState)[K]> {
    return getContext(key);
}
export const createState = {
    userState: (data: UserData) => setContext('userState', new UserState(data)),
    eventHandler: (data: App.PageData) => setContext('eventHandler', new EventHandler(data))
};
