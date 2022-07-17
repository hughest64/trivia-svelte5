/**
 * Import and/or add websocket message handlers functions to this file and
 * export them in the handler object at the bottom. function names (or the key in the handler object)
 * should be in python style snake case and is equivalent to the "type" key in the websocket message
 * functions should take in a data param which is equivalent to the "message" key in the websocekt message.
 */
// import type { Writable } from 'svelte/store';
import { updateResponse } from './response'
import type { MessageHandler } from './types';

// convenience logging function
const log_me = (data: unknown) => console.log(data);

const handlers:MessageHandler = {
    connected: () => undefined, //console.log('connected!'),
    update_response: (data) => updateResponse(data as string),
    log_me,
}

export default handlers