<script lang="ts">
    import { getContext, getAllContexts, onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { createQuestionKey } from '$lib/utils';
    import { PUBLIC_QUESTION_REVEAL_TIMEOUT as updateDelay } from '$env/static/public';
    import type { Writable } from 'svelte/store';
    import type {
        CurrentEventData,
        MessageHandler,
        PopupData,
        QuestionState,
        Response,
        RoundState,
        SocketMessage
    } from './types';

    const allStores = getAllContexts();
    const webSocket = <WebSocket>getContext('socket');

    interface QuestionStateUpdate {
        question_states: QuestionState[];
        event_updated: boolean;
        round_number: number;
        question_number: number;
    }

    const handlers: MessageHandler = {
        connected: () => console.log('connected!'),
        team_response_update: (message: Response) => {
            const responsStore = <Writable<Response[]>>allStores.get('responseData');
            responsStore.update((responses) => {
                const newResponses = [...responses];
                const updateIndex = newResponses.findIndex((response) => response.key === message.key);
                updateIndex > -1
                    ? (newResponses[updateIndex] = { ...newResponses[updateIndex], ...message })
                    : newResponses.push(message);

                return newResponses;
            });
        },
        round_update: (message: RoundState) => {
            const roundStates = <Writable<RoundState[]>>allStores.get('roundStates');
            roundStates.update((states) => {
                const newStates = [...states];
                const roundStateIndex = newStates.findIndex((rs) => rs.round_number === message.round_number);
                if (roundStateIndex > -1) {
                    newStates[roundStateIndex] = message;
                } else {
                    newStates.push(message);
                }

                return newStates;
            });
        },
        question_reveal_popup: (message: Record<string, string | boolean>) => {
            const popupStore = <Writable<PopupData>>allStores.get('popupData');
            const revealed = message.reveal;
            revealed &&
                popupStore.set({
                    is_displayed: true,
                    popup_type: 'question_reveal',
                    timer_value: Math.round(Number(updateDelay) / 1000),
                    data: message
                });
        },
        question_state_update: (message: QuestionStateUpdate) => {
            const questionStateStore = <Writable<QuestionState[]>>allStores.get('questionStates');
            questionStateStore.update((states) => {
                const newStates = [...states];
                message.question_states.forEach((state) => {
                    const currentIndex = newStates.findIndex((qs) => qs.key === state.key);
                    if (currentIndex > -1) {
                        newStates[currentIndex] = state;
                    } else {
                        newStates.push(state);
                    }
                    return true;
                });
                return newStates;
            });
            if (message.event_updated) {
                const currentEventStore = <Writable<CurrentEventData>>allStores.get('currentEventData');
                currentEventStore.set({
                    question_number: message.question_number,
                    round_number: message.round_number,
                    question_key: createQuestionKey(message.round_number, message.question_number)
                });
            }
        },
        current_data_update: (message: CurrentEventData) => {
            const currentDataStore = <Writable<CurrentEventData>>allStores.get('currentEventData');
            currentDataStore.set(message);
        },
        score_update: (message: Record<string, string>) => {
            // TODO: update host AND player reponses, no need to filter by team since ids are unique
            console.log(message);
        }
    };

    onMount(() => {
        webSocket.onmessage = (event) => {
            const data: SocketMessage = JSON.parse(event.data);

            // no active_team_id
            if (data.type === 'unauthorized') {
                // TODO: error message to user?
                goto(`/team?next=${location.pathname}`, { invalidateAll: true });

                // anonymous user in the socket connection
            } else if (data.type === 'unauthenticated') {
                webSocket.send(JSON.stringify({ type: 'authenticate', message: { token: $page.data.jwt } }));
            } else if (handlers[data.type]) {
                handlers[data.type](data.message);
            } else {
                console.error(`message type ${data.type} does not have a handler function!`);
            }
        };
    });
</script>
