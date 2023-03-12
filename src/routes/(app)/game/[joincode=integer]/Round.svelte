<script lang="ts">
    import Question from './Question.svelte';
    import Note from './Note.svelte';
    import { fly } from 'svelte/transition';
    import { sineInOut } from 'svelte/easing';
    import { page } from '$app/stores';
    import { swipeQuestion } from './swipe';
    import { getStore, getQuestionKeys, splitQuestionKey } from '$lib/utils';
    import type { GameQuestion, GameRound } from '$lib/types';

    const joincode = $page.params?.joincode;
    const questions: GameQuestion[] = $page.data.questions || [];

    export let activeRound: GameRound;

    $: activeEventData = getStore('activeEventData');
    $: currentEventData = getStore('currentEventData');
    $: questionKeys = getQuestionKeys($page.data.questions || [], activeRound);

    let swipeDirection = 'right'; // or 'left'
    $: swipeXValue = swipeDirection === 'right' ? 1000 : -4000;
    const inSwipeDuration = 600;
    $: outSwipeDuration = swipeDirection === 'right' ? 100 : 350;

    const allQuestionKeys: string[] = questions.map((q) => q.key);
    const handleQuestionSelect = async (event: MouseEvent | CustomEvent | KeyboardEvent) => {
        const target = <HTMLElement>event.target;
        const eventDirection = event.detail?.direction;
        const keyCode = (event as KeyboardEvent).code;

        let nextQuestionKey = $activeEventData.activeQuestionKey;
        const currentIndex = allQuestionKeys.findIndex((key) => key === nextQuestionKey);
        let nextIndex = -1;

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

        // post to the game endpoint to set active round and question in a cookie
        await fetch('/update', {
            method: 'POST',
            body: JSON.stringify({ activeEventData: $activeEventData, joincode })
        });
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
                <Note />
            </div>
        {/key}
    </div>
</div>
