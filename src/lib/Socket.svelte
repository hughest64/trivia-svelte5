<script lang="ts">
    import { onDestroy, setContext } from 'svelte';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { PUBLIC_QUESTION_REVEAL_TIMEOUT, PUBLIC_WEBSOCKET_HOST } from '$env/static/public';
    import { createQuestionKey, getStore, resolveBool } from '$lib/utils';
    import type {
        CurrentEventData,
        MessageHandler,
        LeaderboardEntry,
        QuestionState,
        Response,
        ResponseSummary,
        RoundState,
        ChatMessage,
        SocketMessage,
        UserTeam,
        TiebreakerResponse,
        TeamNote
    } from './types';
    const path = $page.url.pathname;

    export let socketUrl = `${PUBLIC_WEBSOCKET_HOST}/ws${path}/`;
    export let maxRetries = 50;
    export let retryInterval = 1000;
    export let is_reconnect = false;

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
    const activeEventStore = getStore('activeEventData');
    const currentEventStore = getStore('currentEventData');
    const hostResponseStore = getStore('hostResponseData');
    const responseSummaryStore = getStore('responseSummary');
    const selectedMegaroundStore = getStore('selectedMegaRound');
    const userStore = getStore('userData');
    const tiebreakerResponseStore = getStore('tiebreakerResponses');
    const chatStore = getStore('chatMessages');
    const teamNoteStore = getStore('teamNotes');

    $: isHostEndpoint = $page.url.pathname.startsWith('/host');

    interface HostReminder {
        type: string;
        team_ids?: number[];
    }

    const handlers: MessageHandler = {
        connected: () => console.log('connected!'),
        leaderboard_join: (message: LeaderboardEntry) => {
            leaderboardStore.update((lb) => {
                const newLB = { ...lb };
                const existingPubIndex = lb.public_leaderboard_entries.findIndex((e) => e.team_id === message.team_id);
                existingPubIndex === -1 && newLB.public_leaderboard_entries.push(message);

                // only update the host lb entries on host routes
                if (isHostEndpoint) {
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
            const { tiebreaker_responses, ...leaderboard } = msg;
            const { round_states, ...leaderboardData } = leaderboard;

            leaderboardStore.update((lb) => {
                const newLb = { ...lb };
                Object.assign(newLb, leaderboardData);

                return newLb;
            });

            if (round_states) {
                roundStates.update((states) => {
                    const newStates = [...states];
                    (round_states as RoundState[]).forEach((rs) => {
                        const indexToUpdate = newStates.findIndex((s) => s.round_number === rs.round_number);
                        if (indexToUpdate > -1) newStates[indexToUpdate] = rs;
                    });

                    return newStates;
                });
            }

            if (tiebreaker_responses) {
                tiebreakerResponseStore.update((resps) => {
                    const newResps = [...resps];
                    for (const resp of tiebreaker_responses as TiebreakerResponse[]) {
                        const indexToUpdate = newResps.findIndex((r) => r.id === resp.id) ?? -1;
                        indexToUpdate > -1 ? (newResps[indexToUpdate] = resp) : newResps.push(resp);
                    }
                    return newResps;
                });
            }

            if (!isHostEndpoint) {
                // show a popup for everyone
                popupStore.set({
                    is_displayed: true,
                    popup_type: 'leaderboard_update'
                });
            }
        },
        leaderboard_update_host_entry: (msg: Record<string, LeaderboardEntry | string>) => {
            const updatedEntry = msg.entry as LeaderboardEntry;
            leaderboardStore.update((lb) => {
                const newLb = { ...lb };
                const entries = newLb.host_leaderboard_entries || [];
                const indexToUpdate = entries.findIndex((entry) => entry.team_id === updatedEntry.team_id);
                if (indexToUpdate !== undefined && indexToUpdate > -1) {
                    entries[indexToUpdate] = updatedEntry;
                }

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
        team_note_update: (message: TeamNote) => {
            teamNoteStore.update((notes) => [...notes, message]);
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
                    timer_value: Math.round(Number(PUBLIC_QUESTION_REVEAL_TIMEOUT) / 1000),
                    data: message
                });
        },
        finish_game_popup: () => {
            const highScore =
                $leaderboardStore.public_leaderboard_entries.sort((a, b) => b.total_points - a.total_points)[0]
                    ?.total_points || 0;
            const winners = $leaderboardStore.public_leaderboard_entries.filter(
                (entry) => entry.total_points === highScore
            );
            const names = winners.map((team) => team.team_name);
            popupStore.set({
                is_displayed: true,
                popup_type: 'finish_game',
                data: { winners: names }
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
                if ($userStore.auto_reveal_questions) {
                    activeEventStore.set({
                        activeRoundNumber: message.round_number,
                        activeQuestionNumber: message.question_number,
                        activeQuestionKey: createQuestionKey(message.round_number, message.question_number)
                    });
                }
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
            if (isHostEndpoint) {
                hostResponseStore.update((resps) => {
                    const newResps = [...resps];
                    // all ids should match, but sort the the id array for a bit of insurance
                    const respsToUpdate = newResps.find((resp) => {
                        const exisitngIds = resp.response_ids.sort();
                        const incomingIds = response_ids.sort();

                        return exisitngIds[0] === incomingIds[0];
                    });

                    if (respsToUpdate) {
                        respsToUpdate.points_awarded = Number(points_awarded);
                        respsToUpdate.funny = resolveBool(funny);
                    }
                    return newResps;
                });
                responseStore.update((resps) => {
                    const newResps = [...resps];
                    const respsToUpdate = newResps.filter((resp) => response_ids.includes(resp.id));
                    for (const resp of respsToUpdate) {
                        resp.points_awarded = points_awarded;
                        resp.funny = funny;
                    }

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
        event_megaround_update: (msg: Record<'team_id' | 'selected_megaround', number>) => {
            const { team_id, selected_megaround } = msg;

            leaderboardStore.update((lb) => {
                const newLb = { ...lb };

                const hostEntry = newLb.host_leaderboard_entries?.find((entry) => entry.team_id === team_id);
                hostEntry && (hostEntry.megaround = selected_megaround);

                const publicEntry = newLb.public_leaderboard_entries.find((entry) => entry.team_id === team_id);
                publicEntry && (publicEntry.megaround = selected_megaround);

                return newLb;
            });
        },
        teamname_update: (msg: UserTeam) => {
            console.log(msg);
            leaderboardStore.update((lb) => {
                const newLb = { ...lb };
                const { public_leaderboard_entries, host_leaderboard_entries } = newLb;
                const pubTeamIndex = public_leaderboard_entries.findIndex((entry) => Number(entry.team_id) === msg.id);
                if (pubTeamIndex > -1) {
                    public_leaderboard_entries[pubTeamIndex].team_name = msg.name;
                }

                const hostTeamIndex = host_leaderboard_entries?.findIndex((entry) => Number(entry.team_id) === msg.id);
                if (hostTeamIndex !== undefined && hostTeamIndex > -1) {
                    const entryToUpdate = (host_leaderboard_entries || [])[hostTeamIndex];
                    entryToUpdate.team_name = msg.name;
                }

                return newLb;
            });
            userStore.update((user) => {
                const newUser = { ...user };
                const { teams } = newUser;
                const teamIndex = teams.findIndex((team) => team.id === msg.id);
                if (teamIndex > -1) {
                    teams[teamIndex].name = msg.name;
                }

                return newUser;
            });
        },
        teampassword_update: (msg: UserTeam) => {
            leaderboardStore.update((lb) => {
                const newLb = { ...lb };
                const { public_leaderboard_entries, host_leaderboard_entries } = newLb;
                const pubTeamIndex = public_leaderboard_entries.findIndex((entry) => Number(entry.team_id) === msg.id);
                if (pubTeamIndex > -1) {
                    public_leaderboard_entries[pubTeamIndex].team_name = msg.name;
                }

                const hostTeamIndex = host_leaderboard_entries?.findIndex((entry) => Number(entry.team_id) === msg.id);
                if (hostTeamIndex !== undefined && hostTeamIndex > -1) {
                    const entryToUpdate = (host_leaderboard_entries || [])[hostTeamIndex];
                    entryToUpdate.team_password = msg.password;
                }

                return newLb;
            });
            userStore.update((user) => {
                const newUser = { ...user };
                const { teams } = newUser;
                const teamIndex = teams.findIndex((team) => team.id === msg.id);
                if (teamIndex > -1) {
                    teams[teamIndex].password = msg.password;
                }

                return newUser;
            });
        },
        chat_message: (msg: ChatMessage) => {
            // add to host messages

            if (msg.is_host_message && isHostEndpoint) {
                chatStore.update((chats) => [...chats, msg]);
                return;
            }
            // exit if not a message for the users active team
            if ((!msg.is_host_message && msg.team_id !== $userStore.active_team_id) || isHostEndpoint) return;

            chatStore.update((chats) => {
                const newChats = [...chats];
                const lastChat = chats[chats.length - 1];

                if (!lastChat?.is_host_message && msg.is_host_message) {
                    newChats.push(msg);
                } else if (lastChat?.userid !== msg.userid) {
                    newChats.push(msg);
                } else if (lastChat?.is_host_message && !msg.is_host_message) {
                    newChats.push(msg);
                } else {
                    lastChat.chat_message += '\n' + msg.chat_message;
                    lastChat.time = msg.time;
                }

                return newChats;
            });
        },
        host_reminder: (msg: HostReminder) => {
            if (isHostEndpoint || !msg.team_ids?.includes($userStore.active_team_id as number)) return;

            popupStore.set({
                is_displayed: true,
                popup_type: msg.type
            });
        }
    };

    const createSocket = () => {
        const webSocket = new WebSocket(socketUrl);
        webSocket.onopen = () => {
            clearTimeout(interval);
            retries = 0;
            is_reconnect && window.location.reload();
        };
        webSocket.onclose = (event) => {
            // authentication issue remove the exisitng token if there is one by forcing a logout
            if (event.code === 4010) {
                goto('/user/logout', { invalidateAll: true });
            } else if (!event.wasClean && event.code !== 4010 && retries <= maxRetries) {
                is_reconnect = true;
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
