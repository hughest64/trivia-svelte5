import { getContext, setContext } from 'svelte';
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

// TODO: this a temp store for websocket set up
export const response: Writable<string> = writable();

export const updateResponse = (data: string) => response.set(data);

export const createResponseStore = (): void => {
    setContext('response', writable());
};

export const getResponseStore = (): Writable<string> => {
    return getContext('response');
};
