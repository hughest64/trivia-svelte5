<script lang="ts">
    import { page } from '$app/stores';
    import { createStore } from '$lib/utils';
    import type { ActiveEventData, EventData, Response } from './types';

    $: data = $page.data;
    $: eventData = <EventData>data?.event_data;
    $: responseData = <Response[]>data?.response_data || [];

    // event data
    $: createStore<EventData>('eventData', eventData);

    // active event data
    $: createStore<ActiveEventData>('activeEventData', {
        activeQuestionNumber: data?.activeQuestionNumber || eventData?.current_question_number || 1,
        activeRoundNumber: data?.activeRoundNumber || eventData?.current_question_number || 1
    });

    // TODO: get responses from the server
    $: createStore<Response[]>('responseData', responseData);
</script>

<slot />
