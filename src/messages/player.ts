/**
 * add websocket message handler functions to this file
 * function names (or the key in the handler object) should be in python style snake case
 * and correspond to the "type" key in the websocket message
 * functions should take in a "message" param as well as an optional store to update
 */
import type { Writable } from 'svelte/store';
import type { MessageHandler, PopupData, Response } from '$lib/types';

const handlers: MessageHandler = {
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
                // otherwise add to the end of the list
                currentResponses.push(message);
            }

            return currentResponses;
        });
    },

    // TODO: event handlers maybe should be in a separate file
    event_question_reveal: (message: Record<string, string|boolean>, store: Writable<PopupData>) => {
        // TODO: popupData store
        // console.log(message);
        const revealed = message.value;
        revealed && store.set({ is_displayed: true, popup_type: 'question_reveal', timer_value: 5 });
    }
};

export default handlers;
