<script lang="ts">
    import { fly } from 'svelte/transition';
    import { sineInOut } from 'svelte/easing';
    import { page } from '$app/stores';
    import { swipeQuestion } from './swipe';
    import { getStore } from '$lib/utils';
    import type { ActiveEventData, CurrentEventData, GameQuestion } from '$lib/types';

    const joincode = $page.params?.joincode;
    const questions: GameQuestion[] = $page.data.questions || [];

    $: currentEventData = getStore<CurrentEventData>('currentEventData');
    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: activeQuestionNumber = $activeEventData?.activeQuestionNumber;
    $: activeQuestions = questions.filter((q) => q.round_number === $activeEventData.activeRoundNumber);
    $: questionNumbers = <number[]>activeQuestions.map((q) => q.question_number);
    $: lastQuestionNumber = Math.max(...questionNumbers);

    let swipeDirection = 'right'; // or 'left'
    $: swipeXValue = swipeDirection === 'right' ? 1000 : -4000;

    const inSwipeDuration = 600;
    $: outSwipeDuration = swipeDirection === 'right' ? 100 : 350;

    const handleQuestionSelect = async (event: MouseEvent | CustomEvent | KeyboardEvent) => {
        const target = <HTMLElement>event.target;
        const eventDirection = event.detail?.direction;
        const keyCode = (event as KeyboardEvent).code;
        let nextQuestionNumber = activeQuestionNumber;

        if (eventDirection === 'right' || keyCode === 'ArrowRight') {
            nextQuestionNumber = Math.min(lastQuestionNumber, activeQuestionNumber + 1);
        } else if (eventDirection === 'left' || keyCode === 'ArrowLeft') {
            nextQuestionNumber = Math.max(1, activeQuestionNumber - 1);
        } else if (!!target.id) {
            nextQuestionNumber = Number(target.id);
        }

        swipeDirection = nextQuestionNumber < activeQuestionNumber ? 'left' : 'right';

        activeEventData.update((data) => ({
            ...data,
            activeQuestionNumber: nextQuestionNumber,
            activeQuestionKey: `${$activeEventData.activeRoundNumber}.${nextQuestionNumber}`
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
        {#each questionNumbers as num}
            <!-- TODO: the logic for current isn't quite good enough, we need to condisder the current round as well. -->
            <button
                class="button-white"
                class:current={num === $currentEventData.question_number}
                id={String(num)} on:click={handleQuestionSelect}
            >
                {num}
            </button>
        {/each}
    </div>
    <!-- TODO: transition params in a config object like { left: {...}, right: {...} } -->
    <div class="question-row">
        {#key $activeEventData.activeQuestionKey}
            <div
                class="flex-column question"
                in:fly={{
                    easing: sineInOut,
                    opacity: 100,
                    x: swipeXValue,
                    duration: inSwipeDuration
                }}
                out:fly={{ easing: sineInOut, x: swipeXValue * -1, duration: outSwipeDuration }}
                use:swipeQuestion
                on:swipe={handleQuestionSelect}
            >
                <!-- slot represeents the question and note components -->
                <slot />
            </div>
        {/key}
    </div>
</div>

<style lang="scss">
    .question-box {
        overflow-x: hidden;
        border: 2px solid var(--color-black);
        border-radius: 0.5em;
        width: 50em;
        max-width: calc(100% - 2em);
        margin-top: 1em;
        padding-top: 1em;
        box-shadow: 10px 0px 5px -5px rgb(0 0 0 / 80%);
        & > * {
            max-width: 100%;
        }
    }
    .question-row {
        display: flex;
        justify-content: center;
        width: 100%;
        & > * {
            max-width: 100%;
        }
    }
    .question-selector {
        display: flex;
        gap: 0.5em;
        button {
            font-weight: bold;
            border: 2px solid var(--color-black);
        }
    }
    .question {
        width: 100%;
    }
    button.current {
            border-color: var(--color-current);
        }
</style>
