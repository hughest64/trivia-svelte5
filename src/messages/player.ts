/**
 * add websocket message handler functions to this file
 * function names (or the key in the handler object) should be in python style snake case
 * and correspond to the "type" key in the websocket message
 * functions should take in a "message" param as well as an optional store to update
 */
import type { Writable } from 'svelte/store';
import type { CurrentEventData, MessageHandler, PopupData, Response, RoundState, QuestionState } from '$lib/types';

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
    // TODO: event handlers should be in a separate file
    round_update: (message: Record<string, number | boolean>, store: Writable<RoundState[]>) => {
        store.update((states) => {
            const newStates = [...states];
            const roundState = <RoundState>newStates.find((rs) => rs.round_number === message.round_number);
            roundState.locked = Boolean(message.value);

            return newStates;
        });
    },
    question_reveal: (message: Record<string, string | boolean>, store: Writable<PopupData>) => {
        const revealed = message.value;
        revealed &&
            store.set({
                is_displayed: true,
                popup_type: 'question_reveal',
                timer_value: 5,
                data: { key: message.key }
            });
    },
    question_update: (message: Record<string, string | boolean>, store: Writable<QuestionState[]>) => {
        store.update((states) => {
            const newStates = [...states];
            const updateIndex = states.findIndex((state) => state.key === message.key);
            if (updateIndex > -1) newStates[updateIndex].question_displayed = Boolean(message.value);

            return newStates;
        });
    },
    question_update_all: (message: Record<string, number | boolean>, store: Writable<QuestionState[]>) => {
        store.update((states) => {
            const newStates = [...states];
            newStates.forEach((state) => {
                if (state.round_number === Number(message.round_number)) {
                    state.question_displayed = Boolean(message.value);
                }
                return state;
            });
            return newStates;
        });
    },
    current_data_update: (message: CurrentEventData, store: Writable<CurrentEventData>) => {
        store.set(message);
    }
};

export default handlers;
