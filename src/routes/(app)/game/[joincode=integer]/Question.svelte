<script lang="ts">
    import { page } from '$app/stores';
    import { applyAction, enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import type { ActionData } from './$types';
    import type { GameQuestion, QuestionState, RoundState, Response, UserData } from '$lib/types';

    export let activeQuestion: GameQuestion;
    export let activeResponse: Response | undefined;

    const questionStates = getStore<QuestionState[]>('questionStates');
    $: questionState = $questionStates.find((qs) => qs.key === activeQuestion.key);

    const roundStates = getStore<RoundState[]>('roundStates');
    $: activeRoundState = $roundStates.find((rs) => rs.round_number === activeQuestion.round_number);

    $: responseText = activeResponse?.recorded_answer || '';

    $: form = <ActionData>$page.form;
    $: userData = getStore<UserData>('userData');

    $: notsubmitted = responseText && activeResponse?.recorded_answer !== responseText;
    // event types are rough
    /* eslint-disable-next-line @typescript-eslint/no-explicit-any */
    const handleResponseInput = async (event: any) => {
        const target = <HTMLInputElement>event.target;
        notsubmitted = target.value !== responseText;
    };
</script>

<h2>{activeQuestion.key}</h2>

<p class="question-text">
    {questionState?.question_displayed
        ? activeQuestion.question_text
        : 'Please Wait for the Host to Reveal This Question'}
</p>

<!-- TODO it would be nice to stop submission if the value has not changed, on:submit = () => preventDefault isn't working-->
<form
    action="?/response"
    use:enhance={() =>
        async ({ result }) =>
            await applyAction(result)}
>
    <input type="hidden" name="question_id" value={activeQuestion?.id} />
    <input type="hidden" name="team_id" value={$userData?.active_team_id || ''} />
    <input type="hidden" name="key" value={activeQuestion?.key} />

    <div class="input-element" class:notsubmitted>
        <input disabled={activeRoundState?.locked} required name="response_text" type="text" on:input={handleResponseInput} value={responseText} />
        <label for="response_text">Enter Answer</label>
    </div>

    {#if form?.error}<p>{form.error}</p>{/if}

    <button
        class:disabled={activeRoundState?.locked}
        class="button button-red"
        disabled={activeRoundState?.locked}
    >
        Submit
    </button>
</form>

<style lang="scss">
    h2 {
        margin: 0.5em;
    }

    .question-text {
        padding: 0 1em;
    }

    .notsubmitted {
        input {
            border-color: var(--color-red);
        }
        label {
            background-color: var(--color-red);
        }
    }
    .disabled {
        cursor: not-allowed;
    }
</style>
