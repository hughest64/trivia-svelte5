<script lang="ts">
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import { getStore, setEventCookie } from '$lib/utils';
    import CurrentIcon from './CurrentIcon.svelte';

    const userData = getStore('userData');
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
    const handleGoToCurrent = () => {
        $activeEventData = {
            activeRoundNumber: $currentEventData.round_number,
            activeQuestionNumber: $currentEventData.round_number,
            activeQuestionKey: $currentEventData.question_key
        };
        setEventCookie($activeEventData, $page.params.joincode);
    };
</script>

{#if showGoToCurrent && $activeEventData.activeQuestionKey !== $currentEventData.question_key}
    <div class="question-key-container">
        <span class="spacer" />
        <h4 id={`${questionKey}-key`} class="question-key">{questionKey}</h4>
        <button class="go-to-current" transition:slide on:click={handleGoToCurrent}>
            <CurrentIcon questionKey={$currentEventData.question_key} />
        </button>
    </div>
{:else}
    <h4 id={`${questionKey}-key`} class="question-key">{questionKey}</h4>
{/if}

<style lang="scss">
    .question-key-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: var(--max-element-width);
        max-width: calc(100% - 1rem);
        .spacer {
            width: 5.5rem;
        }
        .go-to-current {
            height: 5.5rem;
            width: 5.5rem;
        }
    }
</style>
