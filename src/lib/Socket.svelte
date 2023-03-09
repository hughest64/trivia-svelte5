<script lang="ts">
    import { getAllContexts, onDestroy, setContext } from 'svelte';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { createQuestionKey } from '$lib/utils';
    import type { Writable } from 'svelte/store';
    import type {
        CurrentEventData,
        MessageHandler,
        LeaderboardEntry,
        PopupData,
        PublicLeaderboard,
        QuestionState,
        Response,
        RoundState,
        SocketMessage
    } from './types';

    const path = $page.url.pathname;

    export let socketUrl = `${$page.data.websocketHost}/ws${path}/`;
    export let maxRetries = 50;
    export let retryInterval = 1000;
    export let reconnect = true;

    let interval: ReturnType<typeof setTimeout>;
    let retries = 0;

    interface QuestionStateUpdate {
        question_states: QuestionState[];
        event_updated: boolean;
        round_number: number;
        question_number: number;
    }

    const allStores = getAllContexts();
    const handlers: MessageHandler = {
        connected: () => console.log('connected!'),
        leaderboard_join: (message: LeaderboardEntry) => {
            const publicStore = <Writable<PublicLeaderboard>>allStores.get('publicLeaderboard');

            publicStore.update((lb) => {
                const newLB = { ...lb };
                const existingIndex = lb.leaderboard_entries.findIndex((e) => e.team_id === message.team_id);
                existingIndex === -1 && newLB.leaderboard_entries.push(message);
                return newLB;
            });
        },
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
                roundStateIndex > -1 ? (newStates[roundStateIndex] = message) : newStates.push(message);

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
                    timer_value: Math.round($page.data.updateDelay / 1000),
                    data: message
                });
        },
        question_state_update: (message: QuestionStateUpdate) => {
            const questionStateStore = <Writable<QuestionState[]>>allStores.get('questionStates');
            questionStateStore.update((states) => {
                const newStates = [...states];
                message.question_states.forEach((state) => {
                    const currentIndex = newStates.findIndex((qs) => qs.key === state.key);
                    currentIndex > -1 ? (newStates[currentIndex] = state) : newStates.push(state);

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
            // TODO: update host AND player responses, no need to filter by team since ids are unique
            console.log(message);
        }
    };

    const createSocket = () => {
        const webSocket = new WebSocket(socketUrl);
        webSocket.onopen = () => {
            clearTimeout(interval);
            retries = 0;
        };
        webSocket.onclose = (event) => {
            // authentication issue remove the exisitng token if there is one by forcing a logout
            if (event.code === 4010) {
                goto('/user/logout', { invalidateAll: true });
            } else if (!event.wasClean && event.code !== 4010 && reconnect && retries <= maxRetries) {
                retries++;
                interval = setTimeout(createSocket, retryInterval);
            } else {
                clearTimeout(interval);
            }
        };
        webSocket.onmessage = (event) => {
            const data: SocketMessage = JSON.parse(event.data);
            const msgType = data.msg_type;

            // no active_team_id
            if (msgType === 'unauthorized') {
                // TODO: error message to user?
                goto(`/team?next=${location.pathname}`, { invalidateAll: true });

                // anonymous user in the socket connection
            } else if (msgType === 'unauthenticated') {
                webSocket.send(JSON.stringify({ type: 'authenticate', message: { token: $page.data.jwt } }));
            } else if (handlers[msgType]) {
                handlers[msgType](data.message);
            } else {
                console.error(`message type ${msgType} does not have a handler function!`);
            }
        };

        return webSocket;
    };

    let socket: WebSocket;
    if (browser) socket = setContext<WebSocket>('socket', createSocket());
    onDestroy(() => socket?.close());
</script>

<slot />
