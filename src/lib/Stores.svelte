<script lang="ts">
    import { page } from '$app/stores';
    import { createStore } from '$lib/utils';
    import type { PopupData } from './types';

    $: data = $page.data;
    $: eventData = data?.event_data;

    $: createStore('userData', data?.user_data || {});
    $: createStore('eventData', eventData || {});
    $: createStore('roundStates', data?.round_states || []);
    $: createStore('questionStates', data?.question_states || []);
    $: createStore('currentEventData', {
        round_number: data?.current_event_data?.round_number || 1,
        question_number: data?.current_event_data?.question_number || 1,
        question_key: data?.current_event_data?.question_key || '1.1'
    });
    $: createStore('activeEventData', {
        activeQuestionNumber: data?.activeQuestionNumber || data.current_event_data?.question_number || 1,
        activeRoundNumber: data?.activeRoundNumber || data.current_event_data?.round_number || 1,
        activeQuestionKey: data?.activeQuestionKey || data.current_event_data?.question_key || '1.1'
    });
    $: createStore('responseData', data?.response_data || []);

    // create an empty popup store
    $: createStore<PopupData>('popupData', { is_displayed: false, popup_type: '' });
</script>

<slot />
