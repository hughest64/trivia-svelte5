<script lang="ts">
    import { page } from '$app/stores';
    import { createStore } from '$lib/utils';
    import type { ActiveEventData, EventData, Response, UserData } from './types';

    $: data = $page.data;
    $: userData = <UserData>data?.user_data;
    $: eventData = <EventData>data?.event_data;
    $: responseData = <Response[]>data?.response_data || [];

    $: createStore<UserData>('userData', userData);

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
