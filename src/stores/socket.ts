import { writable } from "svelte/store";
import type { Writable } from "svelte/store";

export const socket: Writable<WebSocket> = writable();
