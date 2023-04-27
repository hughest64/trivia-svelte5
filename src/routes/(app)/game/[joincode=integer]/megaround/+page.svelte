<script lang="ts">
    import { afterUpdate } from 'svelte';
    import { applyAction, enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import { getMegaroundValues } from '$lib/megaroundValueStore';

    const questions = getStore('questions');
    const rounds = getStore('rounds');
    const responses = getStore('responseData');

    const selectedMegaRound = getStore('selectedMegaRound');
    let activeRoundNumber = $selectedMegaRound;
    let mrResps = $responses.filter((resp) => resp.round_number === activeRoundNumber);
    $: roundQuestions = $questions.filter((q) => q.round_number === activeRoundNumber);

    const roundNumbers = $rounds?.map((rd) => rd.round_number) || [];
    const defaultText = 'You Have not answered this question!';
    let focusedEl: number;

    const mrStore = getStore('megaroundValues');
    // allow resubmission if the active round is already the selected megaround
    let currentMrCleared = false;
    $: allSelected = $mrStore.every((value) => value.used);
    $: submitted = allSelected && activeRoundNumber === $selectedMegaRound && !currentMrCleared;
    $: allowSubmit = !allSelected || submitted;
    $: submitText = submitted ? 'Submitted' : 'Submit';

    const getMegaRoundInput = (qnum?: number): HTMLElement | undefined => {
        const els = document.getElementsByClassName('megaround-weight');
        let inputEl: HTMLInputElement | undefined;

        for (const el of els) {
            if (qnum) {
                if ((el as HTMLElement).dataset.qnum === String(qnum)) {
                    inputEl = el as HTMLInputElement;
                    break;
                }
            } else if (!(el as HTMLInputElement).value) {
                inputEl = el as HTMLInputElement;
                break;
            }
        }
        return inputEl;
    };

    let focused = false;
    const setFocusedEl = (num?: number) => {
        if (num) focused = true;
        const firstEmptyInput = getMegaRoundInput(num);
        focusedEl = Number(firstEmptyInput?.dataset.qnum);
    };

    const handleRoundSelect = (event: MouseEvent) => {
        const roundNum = (event.target as HTMLElement).id;

        activeRoundNumber = Number(roundNum);
        mrResps = $responses.filter((resp) => resp.round_number === activeRoundNumber);
        currentMrCleared = false;

        if (String($selectedMegaRound) === roundNum) {
            const mrValues = getMegaroundValues(mrResps);
            mrStore.set(mrValues);
        } else {
            mrStore.reset();
        }
    };

    const handleSetInputValue = (event: MouseEvent) => {
        const target = event.target as HTMLAreaElement;
        const value = target.id.slice(-1);
        const existingMrValue = mrStore.getValue(value);
        const targetEl = getMegaRoundInput(focusedEl) as HTMLInputElement;

        if (existingMrValue?.used) return;
        mrStore.markUsed(value, targetEl.value);

        if (targetEl) {
            targetEl.value = value;
        }
    };

    const clearValues = () => {
        const els = document.getElementsByClassName('megaround-weight');
        for (const el of els) {
            (el as HTMLInputElement).value = '';
        }
        activeRoundNumber === $selectedMegaRound ? (currentMrCleared = true) : (currentMrCleared = false);
        mrStore.reset();
    };

    afterUpdate(() => {
        !focused && setFocusedEl();
        focused = false;
    });
</script>

<h1>Mega Round</h1>
<small>
    <strong>Instructions: </strong>
    Choose one Mega Round. Then weight each answer 1-5, using each number once. 5 = your most confident answer, 1 = least
    confident.
</small>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        {#if roundNum > roundNumbers.length / 2}
            <button
                class:current={$selectedMegaRound === roundNum}
                class:active={activeRoundNumber === roundNum}
                id={String(roundNum)}
                on:click={handleRoundSelect}
            >
                {roundNum}
            </button>
        {/if}
    {/each}
</div>

{#if $selectedMegaRound && $selectedMegaRound !== activeRoundNumber}
    <h3 class="round-message">Your Currently Selected Mega Round is Round {$selectedMegaRound}</h3>
{/if}

{#if activeRoundNumber}
    <form
        action="?/setmegaround&rd={activeRoundNumber}"
        method="post"
        use:enhance={() =>
            ({ result }) =>
                applyAction(result)}
    >
        {#each roundQuestions as question (question.id)}
            {@const resp = mrResps.find((r) => r.key === question.key)}
            <div class="input-container">
                <input type="hidden" name="question-{question.question_number}" value={question.id} />
                <input
                    type="tel"
                    min="1"
                    max="5"
                    readonly
                    class="megaround-weight"
                    class:focused={focusedEl === question.question_number}
                    id="megaround-weight-{question.question_number}"
                    name="megaround-weight-{question.question_number}"
                    data-qnum={question.question_number}
                    value={resp?.round_number === $selectedMegaRound && resp?.megaround_value
                        ? resp?.megaround_value
                        : ''}
                    on:focus={() => setFocusedEl(question.question_number)}
                />
                <p>{resp?.recorded_answer || defaultText}</p>
            </div>
        {/each}

        <div class="megaround-weight-selector">
            {#each $mrStore as { num, used }}
                <button
                    id="megaround-value-{num}"
                    class="button-white"
                    class:used
                    on:click|preventDefault={handleSetInputValue}>{num}</button
                >
            {/each}
        </div>

        <button type="submit" class="button button-primary" disabled={allowSubmit}>{submitText}</button>
        <button class="button button-secondary" on:click|preventDefault={clearValues}>Clear & Edit</button>
    </form>
{:else}
    <h3>Select A Mega Round!</h3>
{/if}

<style lang="scss">
    small {
        font-size: 16px;
    }
    .round-selector {
        margin: 1rem 0;
    }
    .round-message {
        padding: 0.5rem;
    }
    form {
        .input-container {
            display: flex;
            align-items: center;
            margin: 0.25rem 0;
            padding: 0;
            column-gap: 0.25rem;
            p {
                font-size: 1rem;
                margin: 0;
            }
        }
        input {
            width: 40px;
            height: 40px;
            border: 2px solid var(--color-secondary);
            border-radius: 5px;
            margin: 0;
            margin-right: 0.25rem;
            padding: 0;
            text-align: center;
            &.focused {
                outline: none;
                border-color: var(--color-current);
            }
        }
    }
    .megaround-weight-selector {
        display: flex;
        align-self: center;
        gap: 1rem;
        margin: 1rem 0;
        button {
            width: 3rem;
            height: 3rem;
            font-weight: bold;
            font-size: 1.25rem;
            border: 2px solid var(--color-secondary);
            border-radius: 50%;
            cursor: pointer;
            &.used {
                color: var(--color-alt-white);
                background-color: var(--color-alt-black);
            }
        }
    }
</style>
