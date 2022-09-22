<script lang="ts">
    import { page } from '$app/stores';
    import { createUserStore } from '$stores/user';
    import { createResponseStore } from '$stores/response';
    import { createEventStore, createEventStateStore } from '$stores/event';

    $: data = $page.data;
    $: eventData = data?.event_data;
    
    // user data
    createUserStore(data?.user_data);
    // event data
    createEventStore(eventData);
    // trivia event progress data
    createEventStateStore({
        activeQuestionNumber: data?.activeQuestionNumber || eventData?.currentQuestionNumber,
        activeRoundNumber: data?.activeRoundNumber || eventData?.currentRoundNumber
    });
    createResponseStore();

</script>

<slot />