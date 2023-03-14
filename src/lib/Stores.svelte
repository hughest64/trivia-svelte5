<script lang="ts">
    import { page } from '$app/stores';
    import { readable, writable } from 'svelte/store';
    import { createStore } from '$lib/utils';
    import type { UserData, EventData } from './types';

    $: data = $page.data;

    const userData = createStore('userData', writable(data?.user_data || ({} as UserData)));
    $: data?.user_data && userData.set(data.user_data);

    $: createStore('eventData', readable(data?.event_data || ({} as EventData)));
    $: createStore('rounds', readable($page.data.rounds || []));
    $: createStore('questions', readable($page.data.questions || []));
    $: createStore('popupData', writable({ is_displayed: false, popup_type: '' }));

    // is the player stored as a participant for the event?
    const playerJoined = createStore('playerJoined', writable(false));
    $: playerJoined.set(data.player_joined || false);

    $: createStore(
        'currentEventData',
        writable({
            round_number: data?.current_event_data?.round_number || 1,
            question_number: data?.current_event_data?.question_number || 1,
            question_key: data?.current_event_data?.question_key || '1.1'
        })
    );

    $: createStore(
        'activeEventData',
        writable({
            activeQuestionNumber: data?.activeQuestionNumber || data.current_event_data?.question_number || 1,
            activeRoundNumber: data?.activeRoundNumber || data.current_event_data?.round_number || 1,
            activeQuestionKey: data?.activeQuestionKey || data.current_event_data?.question_key || '1.1'
        })
    );

    $: createStore('roundStates', writable(data?.round_states || []));
    $: createStore('questionStates', writable(data?.question_states || []));
    $: createStore('responseData', writable(data?.response_data || []));

    const publicLeaderboard = createStore('publicLeaderboard', writable());
    $: publicLeaderboard.set(data?.leaderboard_data || {});

    const hostResponses = createStore('hostResponseData', writable([]));
    $: hostResponses.set(data?.host_response_data);
</script>

<slot />
