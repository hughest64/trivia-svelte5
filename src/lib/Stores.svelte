<script lang="ts">
    import { setContext } from 'svelte';
    import { page } from '$app/stores';
    import { readable, writable } from 'svelte/store';
    import { createStore, groupChats } from '$lib/utils';
    import { getMegaroundValues, megaRoundValueStore } from './megaroundValueStore';
    import type { UserData, EventData, LeaderboardEntry } from './types';

    $: isHostPage = $page.url.pathname.startsWith('/host');

    $: data = $page.data;

    const userData = createStore('userData', writable(data?.user_data || ({} as UserData)));
    $: data?.user_data && userData.set(data.user_data);

    $: createStore('eventData', readable(data?.event_data || ({} as EventData)));
    $: createStore('rounds', readable($page.data.rounds || []));
    $: createStore('questions', readable($page.data.questions || []));
    $: createStore('popupData', writable({ is_displayed: false, popup_type: '' }));
    $: createStore('tiebreakerResponses', writable($page.data.tiebreaker_responses || []));
    // group chats for the player side but not the host (which should contain only host messages)
    $: createStore('chatMessages', writable(groupChats($page.data.chat_messages || [], isHostPage)));
    $: createStore('teamNotes', writable($page.data.game_question_notes || []));

    // is the player stored as a participant for the event?
    $: createStore('playerJoined', writable(data.player_joined || false));

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
    // responses grouped for scoring
    $: createStore('hostResponseData', writable(data?.host_response_data || []));

    $: responses = createStore('responseData', writable(data?.response_data || []));
    $: createStore('responseSummary', writable(data?.response_summary || {}));

    $: leaderboardData = data?.leaderboard_data || {};
    $: createStore('leaderboard', writable(leaderboardData));

    $: player_selected_megaround = leaderboardData.public_leaderboard_entries?.find(
        (e: LeaderboardEntry) => e.team_id === $userData.active_team_id
    )?.megaround;
    $: createStore('selectedMegaRound', writable(player_selected_megaround));

    $: player_megaround_responses = $responses.filter((resp) => resp.round_number === player_selected_megaround);
    $: player_used_mr_values = getMegaroundValues(player_megaround_responses);
    $: createStore('megaroundValues', megaRoundValueStore(player_used_mr_values));

    // store a default swipe direction that can be used/updated in multiple components
    // it helps keep the direction in sync when clicking round buttons
    setContext('swipeDirection', writable('left'));
</script>

<slot />
