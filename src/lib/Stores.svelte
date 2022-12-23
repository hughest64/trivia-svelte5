<script lang="ts">
    import { page } from '$app/stores';
    import { createStore } from '$lib/utils';
    import type {
        ActiveEventData,
        CurrentEventData,
        RoundState,
        QuestionState,
        PopupData,
        Response,
        HostResponse
    } from './types';

    $: data = $page.data;

    $: createStore('userData', data?.user_data || {});
    $: createStore('eventData', data?.event_data || {});
    $: createStore<PopupData>('popupData', { is_displayed: false, popup_type: '' });

    $: createStore<CurrentEventData>('currentEventData', {
        round_number: data?.current_event_data?.round_number || 1,
        question_number: data?.current_event_data?.question_number || 1,
        question_key: data?.current_event_data?.question_key || '1.1'
    });

    const activeEventData = createStore<ActiveEventData | null>('activeEventData', null);
    $: activeEventData.set({
        activeQuestionNumber: data?.activeQuestionNumber || data.current_event_data?.question_number || 1,
        activeRoundNumber: data?.activeRoundNumber || data.current_event_data?.round_number || 1,
        activeQuestionKey: data?.activeQuestionKey || data.current_event_data?.question_key || '1.1'
    });

    $: createStore<RoundState[]>('roundStates', data?.round_states || []);
    $: createStore<QuestionState[]>('questionStates', data?.question_states || []);
    $: createStore<Response[]>('responseData', data?.response_data || []);

    const hostResponses = createStore<HostResponse[]>('hostResponseData', []);
    $: hostResponses.set(data?.host_response_data);
</script>

<slot />
