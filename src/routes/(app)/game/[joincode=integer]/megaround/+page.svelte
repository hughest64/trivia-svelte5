<script lang="ts">
    import { afterUpdate } from 'svelte';
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import { applyAction, enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import { getMegaroundValues } from '$lib/megaroundValueStore';

    const joincode = $page.params.joincode;

    const questions = getStore('questions');
    const rounds = getStore('rounds');
    const roundStates = getStore('roundStates');
    const responses = getStore('responseData');
    const playerJoined = getStore('playerJoined');

    const selectedMegaRound = getStore('selectedMegaRound');
    $: activeRoundNumber = $selectedMegaRound;
    $: mrResps = $responses.filter((resp) => resp.round_number === activeRoundNumber);

    // only display locked rounds
    $: roundNumbers = (() => {
        const megaRounds = $rounds.map((rd) => rd.round_number);
        const availableMegaRounds = megaRounds.filter((rdNum) => {
            const rs = $roundStates.find((rs) => rs.round_number === rdNum);
            // either the round state doesn't exist or it isn't locked;
            return rdNum > $rounds.length / 2 && (rs === undefined || (rs.round_number === rdNum && !rs.locked));
        });
        return availableMegaRounds;
    })();

    $: roundQuestions = $questions.filter(
        (q) => q.round_number === activeRoundNumber && roundNumbers.includes(q.round_number)
    );
    const defaultText = 'You Have not answered this question!';
    let focusedEl: number;

    const mrStore = getStore('megaroundValues');
    // allow resubmission if the active round is already the selected megaround
    let currentMrCleared = false;
    $: allSelected = $mrStore.every((value) => value.used);
    $: submitted = allSelected && activeRoundNumber === $selectedMegaRound && !currentMrCleared;
    $: disableSubmit = !allSelected || submitted || !$playerJoined;
    $: submitText = submitted ? 'Submitted' : 'Submit';

    const getMegaRoundInput = (qnum?: number): HTMLElement | undefined => {
        const els = document.getElementsByClassName('megaround-weight') as HTMLCollectionOf<HTMLInputElement>;
        let inputEl: HTMLInputElement | undefined;

        for (const el of els) {
            if (qnum) {
                if (el.dataset.qnum === String(qnum)) {
                    inputEl = el;
                    break;
                }
            } else if (!el.value) {
                inputEl = el;
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

{#if !$playerJoined}
    <h3 out:slide|local class="not-joined-warning">
        <form action="/game/{joincode}?/joinevent" method="post" use:enhance>
            <button class="submit" type="submit"><h3>Click here</h3></button>to join the game!
        </form>
    </h3>
{/if}

{#if $selectedMegaRound && ($selectedMegaRound !== activeRoundNumber || roundNumbers.length < 1)}
    <h3 class="round-message">Your Currently Selected Mega Round is Round {$selectedMegaRound}</h3>
{:else if !activeRoundNumber && roundNumbers.length > 0}
    <h3>Select A Mega Round!</h3>
{/if}

{#if activeRoundNumber && roundQuestions.length > 0}
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
                    class="mr-selector-button"
                    class:used
                    on:click|preventDefault={handleSetInputValue}>{num}</button
                >
            {/each}
        </div>

        <button type="submit" class="button button-primary" disabled={disableSubmit}>{submitText}</button>
        <button
            class="button button-secondary"
            class:disabled={!$playerJoined}
            on:click|preventDefault={clearValues}
            disabled={!$playerJoined}>Clear & Edit</button
        >
    </form>
{/if}

<style lang="scss">
    small {
        font-size: 16px;
    }
    .not-joined-warning {
        width: 100%;
        max-width: var(--max-container-width);
        text-align: center;
        margin-bottom: 0.75rem;
        form {
            display: inline;
        }
        button {
            color: var(--color-primary);
            text-decoration: underline;
        }
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
            padding: 0;
            color: var(--color-secondary);
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
