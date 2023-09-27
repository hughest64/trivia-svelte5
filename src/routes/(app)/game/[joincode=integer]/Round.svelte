<script lang="ts">
    import Question from './Question.svelte';
    // import Note from './Note.svelte';
    import { fly } from 'svelte/transition';
    import { sineInOut } from 'svelte/easing';
    import { page } from '$app/stores';
    import { swipeQuestion } from '$lib/swipe';
    import { getStore, getQuestionKeys, setEventCookie, splitQuestionKey } from '$lib/utils';
    import type { GameRound } from '$lib/types';

    const joincode = $page.params?.joincode;
    const questions = getStore('questions');

    export let activeRound: GameRound;

    const activeEventData = getStore('activeEventData');
    const currentEventData = getStore('currentEventData');
    $: questionKeys = getQuestionKeys($questions || [], activeRound);

    let swipeDirection: 'left' | 'right' = 'right';
    $: swipeXValue = swipeDirection === 'right' ? 1000 : -4000;
    const inSwipeDuration = 600;
    $: outSwipeDuration = swipeDirection === 'right' ? 100 : 350;

    const allQuestionKeys: string[] = $questions.map((q) => q.key);
    const handleQuestionSelect = async (event: MouseEvent | CustomEvent | KeyboardEvent) => {
        const target = <HTMLElement>event.target;
        // allow arrow navigation within the actual text input
        if (target.dataset.type === 'response-input') return;

        const eventDirection = event.detail?.direction;
        const keyCode = (event as KeyboardEvent).code;

        let nextQuestionKey = $activeEventData.activeQuestionKey;
        const currentIndex = allQuestionKeys.findIndex((key) => key === nextQuestionKey);
        let nextIndex = -1;

        if (keyCode !== undefined && keyCode !== 'ArrowLeft' && keyCode !== 'ArrowRight') return;
        if (eventDirection === 'right' || keyCode === 'ArrowRight') {
            nextIndex = currentIndex + 1;
            if (nextIndex < allQuestionKeys.length) {
                nextQuestionKey = allQuestionKeys[nextIndex];
            }
        } else if (eventDirection === 'left' || keyCode === 'ArrowLeft') {
            nextIndex = currentIndex - 1;
            if (nextIndex > -1) {
                nextQuestionKey = allQuestionKeys[nextIndex];
            }
        } else if (target.id) {
            nextQuestionKey = target.id;
        }
        swipeDirection = nextIndex < currentIndex ? 'left' : 'right';

        const { round, question } = splitQuestionKey(nextQuestionKey);
        activeEventData.update((data) => ({
            ...data,
            activeRoundNumber: Number(round),
            activeQuestionNumber: Number(question),
            activeQuestionKey: nextQuestionKey
        }));

        setEventCookie($activeEventData, joincode);
    };
</script>

<svelte:window on:keyup={handleQuestionSelect} />

<div class="question-box flex-column">
    <div class="question-selector">
        {#each questionKeys as key}
            <button
                class="button-white"
                class:current={key === $currentEventData.question_key}
                id={key}
                on:click={handleQuestionSelect}
            >
                {splitQuestionKey(key).question}
            </button>
        {/each}
    </div>

    <div class="question-row">
        {#key $activeEventData.activeQuestionKey}
            <div
                class="flex-column"
                in:fly|local={{
                    easing: sineInOut,
                    opacity: 100,
                    x: swipeXValue,
                    duration: inSwipeDuration
                }}
                out:fly|local={{ easing: sineInOut, x: swipeXValue * -1, duration: outSwipeDuration }}
                use:swipeQuestion
                on:swipe={handleQuestionSelect}
            >
                <Question />
                <!-- <Note /> -->
            </div>
        {/key}
    </div>
</div>
