<script lang="ts">
    import { getContext } from 'svelte';
    import { page } from '$app/stores';
    import { getStore, setEventCookie } from '$lib/utils';
    import CurrentIcon from './CurrentIcon.svelte';
    import type { Writable } from 'svelte/store';

    const userData = getStore('userData');
    const questions = getStore('questions');
    const roundStates = getStore('roundStates');
    const questionStates = getStore('questionStates');
    const currentEventData = getStore('currentEventData');
    const activeEventData = getStore('activeEventData');

    export let questionKey: string = '';

    // track revealed questions in unlocked rounds
    $: lockedRoundNumbers = $roundStates.filter((rs) => rs.locked).map((rs) => rs.round_number);
    $: unlockedRevealedQuestions = $questionStates.filter(
        (qs) => !lockedRoundNumbers.includes(qs.round_number) && qs.question_displayed
    );
    $: showGoToCurrent = !$userData.auto_reveal_questions && unlockedRevealedQuestions.length > 0;

    const swipeDirection = getContext<Writable<'left' | 'right'>>('swipeDirection');
    const questionKeys = $questions.map((q) => q.key);
    const viewingKeyIndex = questionKeys.findIndex((qk) => qk === questionKey);
    const currentKeyIndex = questionKeys.findIndex((qk) => qk === $currentEventData.question_key);

    const handleGoToCurrent = () => {
        swipeDirection.set(viewingKeyIndex > currentKeyIndex ? 'left' : 'right');
        $activeEventData = {
            activeRoundNumber: $currentEventData.round_number,
            activeQuestionNumber: $currentEventData.round_number,
            activeQuestionKey: $currentEventData.question_key
        };
        setEventCookie($activeEventData, $page.params.joincode);
    };
</script>

<div class="question-key-container">
    <span class="spacer" />
    <h4 id={`${questionKey}-key`} class="question-key">{questionKey}</h4>
    {#if showGoToCurrent && $activeEventData.activeQuestionKey !== $currentEventData.question_key}
        <button class="go-to-current" on:click={handleGoToCurrent}>
            <CurrentIcon questionKey={$currentEventData.question_key} />
        </button>
    {:else}
        <span class="spacer" />
    {/if}
</div>

<style lang="scss">
    .question-key-container {
        // outline: 1px dashed purple;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: var(--max-element-width);
        max-width: calc(100% - 1rem);
        .spacer {
            width: 5.5rem;
        }
        .go-to-current {
            margin: 0;
            padding: 0;
        }
    }
</style>
