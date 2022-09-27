<script lang="ts">
    import { page } from '$app/stores';
    import { createStore } from '$lib/utils';
    import { createResponseStore } from '$stores/response';
    import type { EventData, ActiveEventData } from './types';

    $: data = $page.data;
    $: eventData = <EventData>data?.event_data;

    // event data
    $: createStore<EventData>('eventData', eventData);

    // active event data
    $: createStore<ActiveEventData>('activeEventData', {
        activeQuestionNumber: data?.activeQuestionNumber || eventData?.current_question_number || 1,
        activeRoundNumber: data?.activeRoundNumber || eventData?.current_question_number || 1
    });

    createResponseStore();
</script>

<slot />
