<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import AnswerSummary from './AnswerSummary.svelte';
    import type { GameQuestion, Response } from '$lib/types';

    const joincode = $page.params.joincode;

    $: form = $page.form;
    const userData = getStore('userData');
    const activeEventData = getStore('activeEventData');
    const questions = getStore('questions');
    const responses = getStore('responseData') || [];
    const roundStates = getStore('roundStates') || [];
    const questionStates = getStore('questionStates') || [];
    const playerJoined = getStore('playerJoined');

    $: activeQuestion = $questions.find((q) => q.key === $activeEventData.activeQuestionKey) as GameQuestion;
    $: activeResponse = $responses.find((resp) => resp.key === $activeEventData.activeQuestionKey) as Response;
    $: questionState = $questionStates.find((qs) => qs.key === $activeEventData.activeQuestionKey);
    $: activeRoundState = $roundStates.find((rs) => rs.round_number === $activeEventData.activeRoundNumber);

    $: hasImage = activeQuestion?.question_type.toLocaleLowerCase().startsWith('image');

    $: disabled = activeRoundState?.locked || !$playerJoined;
    let responseText = '';
    $: labelText = activeResponse?.recorded_answer ? 'Click To Edit Answer' : 'Enter Answer';
    $: submitText = activeResponse?.recorded_answer ? 'Submitted' : 'Submit';
    $: submitBtnColorClass = activeResponse?.recorded_answer ? 'button-secondary' : 'button-primary';
    $: notsubmitted = responseText && responseText !== activeResponse?.recorded_answer;
    const syncInputText = (e: Event) => {
        const target = <HTMLInputElement>e.target;
        responseText = target.value;
        if (activeResponse?.recorded_answer) {
            if (responseText !== activeResponse.recorded_answer) {
                labelText = 'Update Answer';
                submitText = 'Save';
                submitBtnColorClass = 'button-primary';
            } else {
                labelText = 'Click To Edit Answer';
                submitText = 'Submitted';
                submitBtnColorClass = 'button-secondary';
            }
        }
    };

    const handleSubmitResponse = async () => {
        const data = new FormData();
        data.set('question_id', String(activeQuestion?.id));
        data.set('team_id', String($userData.active_team_id));
        data.set('key', activeQuestion?.key || '');
        data.set('response_text', responseText);

        // TODO: error handling
        await fetch('?/submitresponse', { method: 'post', body: data });
    };
</script>

<h4 id={`${activeQuestion?.key}-key`} class="question-key">{activeQuestion?.key}</h4>

<p id={`${activeQuestion?.key}-text`} class="question-text">
    {questionState?.question_displayed
        ? activeQuestion?.question_text
        : 'Please Wait for the Host to Reveal This Question'}
</p>

{#if hasImage && activeQuestion?.question_url}
    <a href="/game/{joincode}/img?key={activeQuestion.key}" class="button-image">
        <img src={activeQuestion?.question_url} alt="img round" />
    </a>
{:else if hasImage}
    <p>Image Missing</p>
{/if}

{#if activeRoundState?.revealed}
    <AnswerSummary {activeQuestion} {activeResponse} />
{/if}

<form on:submit|preventDefault={handleSubmitResponse}>
    <div id="response-container" class="input-container" class:notsubmitted>
        <input
            {disabled}
            required
            name="response_text"
            type="text"
            autocapitalize="none"
            autocorrect="off"
            autocomplete="off"
            spellcheck="false"
            data-type="response-input"
            value={activeResponse?.recorded_answer || ''}
            on:input={syncInputText}
        />
        <label for="response_text">{disabled ? '' : labelText}</label>
    </div>

    {#if form?.error}<p>{form.error}</p>{/if}

    <button class:disabled class="button {submitBtnColorClass} response-btn" {disabled}> {submitText} </button>
</form>

<style lang="scss">
    .response-btn {
        margin-top: 0;
    }
    img {
        max-width: calc(var(--max-element-width) + 15rem);
        margin: 0 auto;
    }
    .question-text {
        padding: 0 0.5rem;
    }
    .notsubmitted {
        input {
            border-color: var(--color-primary);
        }
        label {
            background-color: var(--color-primary);
        }
    }
</style>
