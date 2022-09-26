<script lang="ts">
    import { page } from '$app/stores';
    import { createUserStore } from '$stores/user';
    import { createStore } from '$lib/utils';
    import { createResponseStore } from '$stores/response';
    import type { EventData, VisibleEventData } from './types';

    $: data = $page.data;
    $: eventData = <EventData>data?.event_data;

    // event data
    createStore<EventData>('eventData', eventData);

    createStore<VisibleEventData>('visibleEventData', {
        activeQuestionNumber: data?.activeQuestionNumber || eventData?.current_question_number || 1,
        activeRoundNumber: data?.activeRoundNumber || eventData?.current_question_number || 1
    });

    // user data
    createUserStore(data?.user_data);
    createResponseStore();
</script>

<slot />
