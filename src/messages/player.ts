/**
 * Import and/or add websocket message handlers functions to this file and
 * export them in the handler object at the bottom. function names (or the key in the handler object)
 * should be in python style snake case and is equivalent to the "type" key in the websocket message
 * functions should take in a data param which is equivalent to the "message" key in the websocekt message.
 */

import type { MessageHandler, StoreType } from '$lib/types';

const handlers: MessageHandler = {
    connected: () => console.log('connected!'), // undefined,
    log_me: (message) => console.log(message),
    set_store: (message, store: StoreType) => store.set(message),
    // TODO: I don't think this works any more than one layer deep, so to lock a round
    // message would need to be all rounds
    update_store: (message, store: StoreType) => store.update((data) => ({ ...data, ...message }))
};

export default handlers;
