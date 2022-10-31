<script lang="ts">
    import { fly } from 'svelte/transition';
    import { sineInOut } from 'svelte/easing';
    import { page } from '$app/stores';
    import { swipeQuestion } from './swipe';
    import type { ActiveEventData, EventRound } from '$lib/types';
    import type { Writable } from 'svelte/store';

    const joincode = $page.params?.joincode;
    export let activeRound: EventRound;
    export let activeData: Writable<ActiveEventData>;
    export let activeQuestionKey: string;
    $: activeQuestionNumber = $activeData?.activeQuestionNumber;

    $: questionNumbers = activeRound?.questions.map((q) => q.question_number);
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
        
        activeData.update((data) => ({ ...data, activeQuestionNumber: nextQuestionNumber }));

        // post to the game endpoint to set active round and question in a cookie
        await fetch('/update', {
            method: 'POST',
            body: JSON.stringify({ activeData: $activeData, joincode })
        });
    };
</script>

<svelte:window on:keyup={handleQuestionSelect} />

<div class="question-box flex-column">
    <div class="question-selector">
        {#each questionNumbers as num}
            <button class="button-white" id={String(num)} on:click={handleQuestionSelect}>{num}</button>
        {/each}
    </div>
    <!-- TODO: transition params in a config object like { left: {...}, right: {...} } -->
    <div class="question-row">
        {#key activeQuestionKey}
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
</style>
