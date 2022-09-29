/**
 * Import and/or add websocket message handlers functions to this file and
 * export them in the handler object at the bottom. function names (or the key in the handler object)
 * should be in python style snake case and is equivalent to the "type" key in the websocket message
 * functions should take in a data param which is equivalent to the "message" key in the websocekt message.
 * 
 * TODO: since a lot will happen in this file, it's probably best to define "getAllStores" and run a filtered
 * version of "getAllContexts" limited to the keys available in the StoreKey interface
 */

import type { Writable } from 'svelte/store';

// TODO: there must be a better way to type this and still be dynmic
export type MessageHandler = Record<string, (message: unknown, store: Writable<unknown>) => unknown>;

// convenience logging function
const log_me = (message: unknown) => console.log(message);

const handlers: MessageHandler = {
    connected: () => console.log('connected!'), // undefined,
    log_me,
    update_response: (message, store) => store.set(message)
};

export default handlers;
