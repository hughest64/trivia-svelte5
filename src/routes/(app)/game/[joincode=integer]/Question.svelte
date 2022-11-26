<script lang="ts">
    import { page } from '$app/stores';
    import { applyAction, enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import type { ActionData } from './$types';
    import type { EventPageData, UserData } from '$lib/types';

    $: eventPageData = getStore<EventPageData>('eventPageData');
    $: activeQuestion = $eventPageData?.activeQuestion;
    $: activeResponse = $eventPageData?.activeResponse;

    $: form = <ActionData>$page.form;
    $: userData = getStore<UserData>('userData');

    $: questionState = $eventPageData.activeQuestionState;
    $: activeRoundState = $eventPageData.activeRoundState;

    // TODO: this is an awful lot just to get a different class applied
    $: responseText = activeResponse?.recorded_answer || '';
    $: updatedInputText = responseText;
    $: notsubmitted = updatedInputText !== responseText;
    const syncInputText = (e: Event) => {
        const target = <HTMLInputElement>e.target;
        updatedInputText = target.value;
    };
</script>

<h2>{activeQuestion?.key}</h2>

<p id={`${activeQuestion?.key}-text`} class="question-text">
    {questionState?.question_displayed
        ? activeQuestion?.question_text
        : 'Please Wait for the Host to Reveal This Question'}
</p>

<!-- TODO it would be nice to stop submission if the value has not changed, on:submit = () => preventDefault isn't working-->
<!-- TODO: change this to preveDefault w/ a handle function like host side, I think native behavior is problematic here -->
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
        <input
            disabled={activeRoundState?.locked}
            required
            name="response_text"
            type="text"
            value={responseText}
            on:input={syncInputText}
        />
        <label for="response_text">Enter Answer</label>
    </div>

    {#if form?.error}<p>{form.error}</p>{/if}

    <button class:disabled={activeRoundState?.locked} class="button button-red" disabled={activeRoundState?.locked}>
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
