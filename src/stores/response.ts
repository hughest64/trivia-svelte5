import { writable } from "svelte/store";
import type { Writable } from 'svelte/store'

// TODO: this a temp store for websocket set up
export const response: Writable<string> = writable();

// TODO: is there a better way to set types here?
export const updateResponse = (data: string) => response.set(data);
