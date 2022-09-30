/**
 * Import and/or add websocket message handlers functions to this file and
 * export them in the handler object at the bottom. function names (or the key in the handler object)
 * should be in python style snake case and is equivalent to the "type" key in the websocket message
 * functions should take in a data param which is equivalent to the "message" key in the websocekt message.
 */

import type { Writable } from 'svelte/store';
import type { SocketMessage, /** AllStores */ } from '$lib/types';

export type MessageHandler = Record<
    string,
    (message: SocketMessage['message'], store: Writable<typeof message>) => unknown
>;

// convenience logging function
const log_me = (message: SocketMessage['message']) => console.log(message);

const handlers: MessageHandler = {
    connected: () => console.log('connected!'), // undefined,
    log_me,
    // this could be use as a generic store setter/updater
    update_store: (message, store) => store.set(message)
};

export default handlers;
