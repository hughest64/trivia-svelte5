/**
 * Import and/or add websocket message handlers functions to this file and
 * export them in the handler object at the bottom. function names (or the key in the handler object)
 * should be in python style snake case and is equivalent to the "type" key in the websocket message
 * functions should take in a data param which is equivalent to the "message" key in the websocekt message.
 */

import type { MessageHandler } from '$lib/types';

const handlers: MessageHandler = {
    connected: () => console.log('connected!'), // undefined,
    log_me: (message) => console.log(message),
    update_store: (message, store) => store.set(message)
};

export default handlers;
