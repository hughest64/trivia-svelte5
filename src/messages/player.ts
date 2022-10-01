/**
 * Import and/or add websocket message handlers functions to this file and
 * export them in the handler object at the bottom. function names (or the key in the handler object)
 * should be in python style snake case and is equivalent to the "type" key in the websocket message
 * functions should take in a data param which is equivalent to the "message" key in the websocekt message.
 */

import type { SocketMessage, StoreType } from '$lib/types';

export type MessageHandler = Record<
    string,
    (message: SocketMessage['message'], store: StoreType) => unknown
>;

// convenience logging function
const log_me = (message: SocketMessage['message']) => console.log(message);

const handlers: MessageHandler = {
    connected: () => console.log('connected!'), // undefined,
    log_me,
    update_store: (message, store) => store.set(message)
};

export default handlers;
