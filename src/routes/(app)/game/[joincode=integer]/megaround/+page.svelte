<script lang="ts">
    import { onMount } from 'svelte';
    import { applyAction, enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import { defaultMegaroundValues, megaRoundValueStore } from './megaroundValueStore';

    const questions = getStore('questions');
    const rounds = getStore('rounds');
    const responses = getStore('responseData');

    // TODO: get value from the store
    const selectedMegaRound = 5;
    let selectedRoundNumber = 5; // : number;
    $: roundQuestions = $questions.filter((q) => q.round_number === selectedRoundNumber);

    const roundNumbers = $rounds?.map((rd) => rd.round_number) || [];
    const defaultText = 'You Have not answered this question!';
    let focusedEl: number;

    // TODO: possibly move this and create it in Stores.svelte same as all others
    // use leaderbaord entry and existing responses to populate an intial value
    $: mrStore = megaRoundValueStore();

    const getMegaRoundInput = (qnum?: number): HTMLElement | undefined => {
        const els = document.getElementsByClassName('megaround-weight');
        let inputEl: HTMLElement | undefined;

        for (const el of els) {
            if (qnum) {
                if ((el as HTMLElement).dataset.qnum === String(qnum)) {
                    inputEl = el as HTMLElement;
                    break;
                }
            } else if (!(el as HTMLElement).dataset.mrvalue) {
                inputEl = el as HTMLElement;
                break;
            }
        }
        return inputEl;
    };

    const setFocusedEl = () => {
        const firstEmptyInput = getMegaRoundInput();
        focusedEl = Number(firstEmptyInput?.dataset.qnum);
    };

    const handleRoundSelect = (event: MouseEvent) => {
        const roundNum = (event.target as HTMLElement).id;
        selectedRoundNumber = Number(roundNum);
        clearValues();
        setFocusedEl();
        // TODO: this need to respect pre-filled values, i.e. if a player navigates to their
        // selected megaround, used should be true as necessary
        mrStore.reset();
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
            targetEl.dataset.mrvalue = value;
        }
        setFocusedEl();
    };

    const clearValues = () => {
        const els = document.getElementsByClassName('megaround-weight');
        for (const el of els) {
            (el as HTMLInputElement).value = '';
            (el as HTMLInputElement).dataset.mrvalue = '';
        }
        mrStore.reset();
        setFocusedEl();
    };

    onMount(setFocusedEl);
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
                class:current={selectedMegaRound === roundNum}
                class:active={selectedRoundNumber === roundNum}
                id={String(roundNum)}
                on:click={handleRoundSelect}
            >
                {roundNum}
            </button>
        {/if}
    {/each}
</div>

<!-- keyboard is disabled, must use -->
{#if selectedRoundNumber}
    <form
        action="?/setmegaround"
        method="post"
        use:enhance={() =>
            ({ result }) =>
                applyAction(result)}
    >
        {#each roundQuestions as question (question.id)}
            {@const resp = $responses.find((r) => r.key === question.key)}
            <div class="input-container">
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
                    data-mrvalue={resp?.mega_round_value || ''}
                    value={resp?.mega_round_value || ''}
                    on:focus={() => (focusedEl = question.question_number)}
                />
                <p>{resp?.recorded_answer || defaultText}</p>
            </div>
        {/each}

        <div class="megaround-weight-selector">
            {#each $mrStore || defaultMegaroundValues as { num, used }}
                <button
                    id="megaround-value-{num}"
                    class="button-white"
                    class:used
                    on:click|preventDefault={handleSetInputValue}>{num}</button
                >
            {/each}
        </div>

        <!-- TODO submit button should be disabled until all fields are filled in -->
        <button type="submit" class="button button-primary">Submit</button>
        <button class="button button-secondary" on:click|preventDefault={clearValues}>Clear & Edit</button>
    </form>
{/if}

<style lang="scss">
    small {
        font-size: 16px;
    }
    .round-selector {
        margin: 1rem 0;
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
                // caret-color: transparent;
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
