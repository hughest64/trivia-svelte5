<script lang="ts">
    import { fly } from 'svelte/transition';
    import { sineInOut } from 'svelte/easing';
    import { page } from '$app/stores';
    import { swipeQuestion } from './swipe';
    import { getStore, splitQuestionKey } from '$lib/utils';
    import type { ActiveEventData, EventPageData, GameQuestion } from '$lib/types';

    const joincode = $page.params?.joincode;
    const questions: GameQuestion[] = $page.data.questions || [];

    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: eventPageData = getStore<EventPageData>('eventPageData');
    $: questionKeys = $eventPageData.questionKeys;

    let swipeDirection = 'right'; // or 'left'
    $: swipeXValue = swipeDirection === 'right' ? 1000 : -4000;
    const inSwipeDuration = 600;
    $: outSwipeDuration = swipeDirection === 'right' ? 100 : 350;

    const allQuestionKeys: string[] = questions.map((q) => q.key);
    const handleQuestionSelect = async (event: MouseEvent | CustomEvent | KeyboardEvent) => {
        const target = <HTMLElement>event.target;
        const eventDirection = event.detail?.direction;
        const keyCode = (event as KeyboardEvent).code;

        let nextQuestionKey = $eventPageData.activeQuestionKey;
        let currentIndex = allQuestionKeys.findIndex((key) => key === nextQuestionKey);
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
            <!-- TODO: the logic for current isn't quite good enough, we need to condisder the current round as well. -->
            <button
                class="button-white"
                class:current={key === $eventPageData.currentQuestionKey}
                id={key}
                on:click={handleQuestionSelect}
            >
                {splitQuestionKey(key).question}
            </button>
        {/each}
    </div>
    <!-- TODO: transition params in a config object like { left: {...}, right: {...} } -->
    <div class="question-row">
        {#key $activeEventData.activeQuestionKey}
            <div
                class="flex-column question"
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
                <!-- slot represents the question and note components -->
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
            width: 2.5em;
            height: 2.5em;
            font-weight: bold;
            border: 2px solid var(--color-black);
            border-radius: 50%;
            cursor: pointer;
        }
    }
    .question {
        width: 100%;
    }
    button.current {
        border-color: var(--color-current);
    }
</style>
