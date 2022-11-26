<script lang="ts">
    import { getContext, getAllContexts, onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
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
        round_update: (message: Record<string, number | boolean>) => {
            const roundStates = <Writable<RoundState[]>>allStores.get('roundStates');
            roundStates.update((states) => {
                const newStates = [...states];
                const roundState = newStates.find((rs) => rs.round_number === message.round_number);
                if (roundState) roundState.locked = Boolean(message.value);

                return newStates;
            });
        },
        question_reveal_popup: (message: Record<string, string | boolean>) => {
            const popupStore = <Writable<PopupData>>allStores.get('popupData');
            const revealed = message.value;
            revealed &&
                popupStore.set({
                    is_displayed: true,
                    popup_type: 'question_reveal',
                    timer_value: Math.round(Number(updateDelay) / 1000),
                    data: { key: message.key }
                });
        },
        question_update: (message: Record<string, string | boolean>) => {
            const questionStateStore = <Writable<QuestionState[]>>allStores.get('questionStates');
            questionStateStore.update((states) => {
                const newStates = [...states];
                const updateIndex = states.findIndex((state) => state.key === message.key);
                if (updateIndex > -1) newStates[updateIndex].question_displayed = Boolean(message.value);

                return newStates;
            });
        },
        question_update_all: (message: Record<string, number | boolean>) => {
            const questionStateStore = <Writable<QuestionState[]>>allStores.get('questionStates');
            questionStateStore.update((states) => {
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
        current_data_update: (message: CurrentEventData) => {
            const currentDataStore = <Writable<CurrentEventData>>allStores.get('currentEventData');
            currentDataStore.set(message);
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
        // TODO: returm webSocket.close()?
    });
</script>
