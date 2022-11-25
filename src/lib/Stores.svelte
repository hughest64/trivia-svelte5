<script lang="ts">
    import { page } from '$app/stores';
    import { createStore } from '$lib/utils';
    import type { ActiveEventData, RoundState, QuestionState, PopupData, Response } from './types';

    $: data = $page.data;

    $: createStore('userData', data?.user_data || {});
    $: createStore('eventData', data?.event_data || {});
    // create an empty popup store
    $: createStore<PopupData>('popupData', { is_displayed: false, popup_type: '' });
    $: createStore('currentEventData', {
        round_number: data?.current_event_data?.round_number || 1,
        question_number: data?.current_event_data?.question_number || 1,
        question_key: data?.current_event_data?.question_key || '1.1'
    });
    $: actveEventData = createStore<ActiveEventData>('activeEventData', {
        activeQuestionNumber: data?.activeQuestionNumber || data.current_event_data?.question_number || 1,
        activeRoundNumber: data?.activeRoundNumber || data.current_event_data?.round_number || 1,
        activeQuestionKey: data?.activeQuestionKey || data.current_event_data?.question_key || '1.1'
    });
    $: roundStates = createStore<RoundState[]>('roundStates', data?.round_states || []);
    $: questionStates = createStore<QuestionState[]>('questionStates', data?.question_states || []);
    $: responses = createStore<Response[]>('responseData', data?.response_data || []);

    // TODO: make a store w/ a good name
    $: eventPageData = {
        roundNumbers: data.rounds?.map((rd) => rd.round_number),
        activeRound: data.rounds?.find((rd) => rd.round_number === $actveEventData.activeRoundNumber),
        activeRoundQuestionNumbers: data.questions
            ?.filter((q) => q.round_number === $actveEventData.activeRoundNumber)
            .map((q) => q.question_number),
        activeRoundState: $roundStates.find((rs) => rs.round_number === $actveEventData.activeRoundNumber),
        activeQuestion: data.questions?.find((q) => q.key === $actveEventData.activeQuestionKey),
        activeQuestionState: $questionStates.find((qs) => qs.key === $actveEventData.activeQuestionKey),
        activeResponse: $responses.find((response) => response.key === $actveEventData.activeQuestionKey)
    };
</script>

<slot />
