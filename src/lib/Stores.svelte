<script lang="ts">
    import { page } from '$app/stores';
    import { createStore } from '$lib/utils';
    import type { PopupData, ActiveEventData, EventData } from './types';

    $: data = $page.data;
    $: eventData = <EventData>data?.event_data;

    $: createStore('userData', data?.user_data || {});
    $: createStore('eventData', eventData || {});
    $: createStore('roundStates', data?.round_states || []);
    $: createStore('questionStates', data?.question_states || []);

    // active event data
    $: createStore<ActiveEventData>('activeEventData', {
        activeQuestionNumber: data?.activeQuestionNumber || eventData?.current_question_number || 1,
        activeRoundNumber: data?.activeRoundNumber || eventData?.current_question_number || 1,
        activeQuestionKey: data?.activeQuestionKey || '1.1'
    });
    $: createStore('responseData', data?.response_data || []);

    // create a generic popup store
    $: createStore<PopupData>('popupData', { is_displayed: false, popup_type: '' });
</script>

<slot />
