<script lang="ts">
    import { getStore } from '$lib/utils';
    import RoundHeader from '$lib/game/RoundHeader.svelte';
    import Round from '$lib/game/Round.svelte';
    import Question from '$lib/game/Question.svelte';
    import Note from '$lib/game/Note.svelte';
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
    <Question {activeRound} {activeQuestion} />
    <Note activeRoundNumber={activeRound.round_number} activeQuestionNumber={activeQuestion.question_number} />
</Round>
