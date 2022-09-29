<script lang="ts">
    import { getStore } from '$lib/utils';
    import RoundHeader from './RoundHeader.svelte';
    import Round from './Round.svelte';
    import Question from './Question.svelte';
    import Note from './Note.svelte';
    import type { ActiveEventData, EventData } from '$lib/types';

    $: activeData = getStore<ActiveEventData>('activeEventData');
    $: eventData = getStore<EventData>('eventData');

    $: activeRound =
        $eventData?.rounds.find((round) => round.round_number === $activeData.activeRoundNumber) ||
        $eventData.rounds[0];

    $: activeQuestion =
        activeRound.questions.find((question) => question.question_number === $activeData.activeQuestionNumber) ||
        activeRound?.questions[0];

    $: roundNumbers = $eventData?.rounds.map((round) => round.round_number);
</script>

<RoundHeader {activeData} {eventData} {activeRound} {roundNumbers} />
<Round {activeRound} {activeData}>
    <Question activeRoundNumber={activeRound.round_number} {activeQuestion} />
    <Note activeRoundNumber={activeRound.round_number} activeQuestionNumber={activeQuestion.question_number} />
</Round>
