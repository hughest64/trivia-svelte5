<script lang="ts">
    import { onDestroy, setContext } from 'svelte';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { createQuestionKey, getStore, resolveBool } from '$lib/utils';
    import type {
        CurrentEventData,
        MessageHandler,
        LeaderboardEntry,
        QuestionState,
        Response,
        ResponseSummary,
        RoundState,
        SocketMessage,
        HostResponse,
        HostMegaRoundInstance
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

    const leaderboardStore = getStore('leaderboard');
    const responseStore = getStore('responseData');
    const roundStates = getStore('roundStates');
    const popupStore = getStore('popupData');
    const questionStateStore = getStore('questionStates');
    const currentEventStore = getStore('currentEventData');
    const hostResponseStore = getStore('hostResponseData');
    const responseSummaryStore = getStore('responseSummary');
    const selectedMegaroundStore = getStore('selectedMegaRound');

    const handlers: MessageHandler = {
        connected: () => console.log('connected!'),
        leaderboard_join: (message: LeaderboardEntry) => {
            leaderboardStore.update((lb) => {
                const newLB = { ...lb };
                const existingPubIndex = lb.public_leaderboard_entries.findIndex((e) => e.team_id === message.team_id);
                existingPubIndex === -1 && newLB.public_leaderboard_entries.push(message);

                // only update the host lb entries on host routes
                if ($page.url.pathname.startsWith('/host')) {
                    const existingHostIndex = lb.host_leaderboard_entries?.findIndex(
                        (e) => e.team_id === message.team_id
                    );
                    existingHostIndex === -1 && newLB.host_leaderboard_entries?.push(message);
                }
                return newLB;
            });
        },
        // TODO: better typings
        leaderboard_update: (msg: Record<string, unknown>) => {
            const { ...leaderboard } = msg;
            leaderboardStore.update((lb) => {
                const newLb = { ...lb };
                Object.assign(newLb, leaderboard);

                return newLb;
            });
        },
        team_response_update: (message: Response) => {
            responseStore.update((responses) => {
                const newResponses = [...responses];
                const updateIndex = newResponses.findIndex((response) => response.key === message.key);
                updateIndex > -1
                    ? (newResponses[updateIndex] = { ...newResponses[updateIndex], ...message })
                    : newResponses.push(message);

                return newResponses;
            });
        },
        round_update: (message: Record<string, RoundState | Response[] | ResponseSummary>) => {
            const updatedRoundState = <RoundState>message.round_state;
            roundStates.update((states) => {
                const newStates = states ? [...states] : [];
                const roundStateIndex = newStates.findIndex((rs) => rs.round_number === updatedRoundState.round_number);
                roundStateIndex > -1
                    ? (newStates[roundStateIndex] = updatedRoundState)
                    : newStates.push(updatedRoundState);

                return newStates;
            });
            // update player responses based on id
            if (updatedRoundState.locked) {
                const responses = <Response[]>message.responses;
                responseStore.update((resps) => {
                    const newResps = [...resps];
                    responses.forEach((updatedResp) => {
                        const respIndex = newResps.findIndex((resp) => resp.id === updatedResp.id);
                        if (respIndex > -1) newResps[respIndex] = updatedResp;
                    });

                    return newResps;
                });
                responseSummaryStore.set(message.response_summary as ResponseSummary);
            }
        },
        round_state_update: (message: Record<string, RoundState[]>) => {
            roundStates.set(message.round_states);
        },
        question_reveal_popup: (message: Record<string, string | boolean>) => {
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
                currentEventStore.set({
                    question_number: message.question_number,
                    round_number: message.round_number,
                    question_key: createQuestionKey(message.round_number, message.question_number)
                });
            }
        },
        current_data_update: (message: CurrentEventData) => {
            currentEventStore.set(message);
        },

        // TODO: a better type for message here
        /* eslint-disable @typescript-eslint/no-explicit-any*/
        score_update: (message: Record<string, any>) => {
            const { response_ids, points_awarded, funny, question_key, leaderboard_data, response_summary } = message;

            // update the response summary TODO: this should be selective for more efficient db processing
            if (response_summary) {
                responseSummaryStore.set(response_summary);
            }

            // update team response if appropriate
            if ($page.url.pathname.startsWith('/game')) {
                responseStore.update((resps) => {
                    const newResps = [...resps];
                    const respToUpdate = resps.find((resp) => resp.key === question_key) as Response;

                    if (respToUpdate) {
                        respToUpdate.points_awarded = points_awarded;
                        respToUpdate.funny = resolveBool(funny);
                    }

                    return newResps;
                });
            }

            // update host reponses if appropriate
            if ($page.url.pathname.startsWith('/host')) {
                hostResponseStore.update((resps) => {
                    const newResps = [...resps];
                    // TODO: it seems likely that relying in the first index to match is not a good idea!
                    const respsToUpdate =
                        newResps.find((resp) => resp.response_ids[0] === response_ids[0]) || ({} as HostResponse);
                    respsToUpdate.points_awarded = Number(points_awarded);
                    respsToUpdate.funny = resolveBool(funny);
                    return newResps;
                });
                if (leaderboard_data) {
                    leaderboardStore.update((lb) => {
                        const newLb = { ...lb };
                        Object.assign(newLb, leaderboard_data);

                        return newLb;
                    });
                }
            }
        },
        team_megaround_update: (message: any) => {
            const { responses, selected_megaround } = message;

            responseStore.update((currentResponses) => {
                const newResponses = [...currentResponses];
                (responses as Response[]).forEach((resp) => {
                    const updateIndex = newResponses.findIndex((response) => response.key === resp.key);
                    updateIndex > -1
                        ? (newResponses[updateIndex] = { ...newResponses[updateIndex], ...resp })
                        : newResponses.push(resp);
                });

                return newResponses;
            });

            selectedMegaroundStore.set(selected_megaround);
        },
        host_megaround_update: (msg: HostMegaRoundInstance) => {
            // only update host routes
            if (!$page.url.pathname.startsWith('/host')) return;

            leaderboardStore.update((lb) => {
                const newLb = { ...lb };
                const megaroundList = newLb.host_megaround_list || [];
                const indexToUpdate = megaroundList.findIndex((e) => e.team_id === msg.team_id);
                indexToUpdate > -1 ? (megaroundList[indexToUpdate] = msg) : megaroundList?.push(msg);
                newLb.host_megaround_list = megaroundList;
                return newLb;
            });
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
