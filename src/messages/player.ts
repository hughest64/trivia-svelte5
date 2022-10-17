/**
 * Import and/or add websocket message handlers functions to this file and
 * export them in the handler object at the bottom. function names (or the key in the handler object)
 * should be in python style snake case and is equivalent to the "type" key in the websocket message
 * functions should take in a data param which is equivalent to the "message" key in the websocekt message.
 */
import { get } from 'svelte/store';
import type { Writable } from 'svelte/store';
import type { AllStores, Response, StoreType } from '$lib/types';

const handlers: Record<string, any> = {
    connected: () => console.log('connected!'), // undefined,
    log_me: (message: AllStores) => console.log(message),
    set_store: (message: AllStores, store: StoreType) => store.set(message),
    // TODO: I don't think this works any more than one layer deep, so to lock a round
    // message would need to be all rounds
    update_store: (message: AllStores, store: StoreType) => store.update((data) => ({ ...data, ...message })),

    team_update_response: (message: Response, store: Writable<Response[]>) => {
    
        store.update((responses) => {
            console.log(responses);
            const responseIndex = responses.findIndex((response) => response.key === message.key);
            console.log(responseIndex);
            const currentResponses = [...responses];
    
            let response_to_update: Response;
            if (responseIndex > -1) {
                response_to_update = currentResponses.splice(responseIndex, 1)[0];
                Object.assign(response_to_update, message);
            } else {
                response_to_update = message;
            }
            currentResponses.push(response_to_update);
            console.log(currentResponses);
            
            return currentResponses;
        });
    }
};

export default handlers;
