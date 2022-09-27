<script lang="ts">
    import { page } from '$app/stores';
    import { createStore } from '$lib/utils';
    import { createResponseStore } from '$stores/response';
    import type { EventData, ActiveEventData } from './types';

    $: data = $page.data;
    $: eventData = <EventData>data?.event_data;

    // event data
    // TODO: the reactive assigment seems annoyingly requried here as I
    // think we don't initially have the game data from prerendering?
    $: _ = createStore<EventData>('eventData', eventData);

    createStore<ActiveEventData>('activeEventData', {
        activeQuestionNumber: data?.activeQuestionNumber || eventData?.current_question_number || 1,
        activeRoundNumber: data?.activeRoundNumber || eventData?.current_question_number || 1
    });

    createResponseStore();
</script>

<slot />
