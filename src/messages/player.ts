/**
 * Import and/or add websocket message handlers functions to this file and
 * export them in the handler object at the bottom. function names (or the key in the handler object)
 * should be in python style snake case and is equivalent to the "type" key in the websocket message
 * functions should take in a data param which is equivalent to the "message" key in the websocekt message.
 */
import type { Writable } from 'svelte/store';
import type { Response } from '$lib/types';

/* eslint-disable-next-line @typescript-eslint/no-explicit-any*/
const handlers: Record<string, (message: any, store: Writable<any>) => unknown> = {
    connected: () => console.log('connected!'), // undefined,
    log_me: (message) => console.log(message),
    set_store: (message, store) => store.set(message),
    team_update_response: (message: Response, store: Writable<Response[]>) => {
        store.update((responses) => {
            const responseIndex = responses.findIndex((response) => response.key === message.key);
            const currentResponses = [...responses];

            if (responseIndex > -1) {
                // keep the original index if the response exists
                currentResponses.splice(responseIndex, 1, { ...currentResponses[responseIndex], ...message });
            } else {
                // add to the end of the list
                currentResponses.push(message);
            }

            return currentResponses;
        });
    }
};

export default handlers;
