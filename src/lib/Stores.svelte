<script lang="ts">
    import { page } from '$app/stores';
    import { createStore } from '$lib/utils';
    import type {
        ActiveEventData,
        CurrentEventData,
        EventPageData,
        RoundState,
        QuestionState,
        PopupData,
        Response
    } from './types';

    $: data = $page.data;

    $: createStore('userData', data?.user_data || {});
    $: createStore('eventData', data?.event_data || {});
    $: createStore<PopupData>('popupData', { is_displayed: false, popup_type: '' });

    $: currentEventData = createStore<CurrentEventData>('currentEventData', {
        round_number: data?.current_event_data?.round_number || 1,
        question_number: data?.current_event_data?.question_number || 1,
        question_key: data?.current_event_data?.question_key || '1.1'
    });

    $: activeEventData = createStore<ActiveEventData>('activeEventData', {
        activeQuestionNumber: data?.activeQuestionNumber || data.current_event_data?.question_number || 1,
        activeRoundNumber: data?.activeRoundNumber || data.current_event_data?.round_number || 1,
        activeQuestionKey: data?.activeQuestionKey || data.current_event_data?.question_key || '1.1'
    });

    $: roundStates = createStore<RoundState[]>('roundStates', data?.round_states || []);
    $: questionStates = createStore<QuestionState[]>('questionStates', data?.question_states || []);
    $: responses = createStore<Response[]>('responseData', data?.response_data || []);

    // create the store and set it reactively, this allows changes to active event data to update the store
    $: eventPageData = createStore<EventPageData | null>('eventPageData', null);
    $: eventPageData.set({
        roundNumbers: data.rounds?.map((rd) => rd.round_number) || [],
        activeRound: data.rounds?.find((rd) => rd.round_number === $activeEventData.activeRoundNumber),
        questionKeys:
            data.questions
                ?.filter((q) => q.round_number === $activeEventData.activeRoundNumber)
                .map((q) => q.key) || [],
        activeRoundState: $roundStates.find((rs) => rs.round_number === $activeEventData.activeRoundNumber),
        activeQuestion: data.questions?.find((q) => q.key === $activeEventData.activeQuestionKey),
        activeQuestionState: $questionStates.find((qs) => qs.key === $activeEventData.activeQuestionKey),
        activeResponse: $responses.find((response) => response.key === $activeEventData.activeQuestionKey),
        activeRoundNumber: $activeEventData.activeRoundNumber,
        activeQuestionKey: $activeEventData.activeQuestionKey,
        currentRoundNumber: $currentEventData.round_number,
        currentQuestionKey: $currentEventData.question_key
    });
</script>

<slot />
