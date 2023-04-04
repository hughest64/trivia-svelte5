<script lang="ts">
    import Lightbox from '$lib/Lightbox.svelte';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';

    $: form = $page.form;
    const userData = getStore('userData');
    const activeEventData = getStore('activeEventData');
    const questions = getStore('questions');
    const responses = getStore('responseData') || [];
    const roundStates = getStore('roundStates') || [];
    const questionStates = getStore('questionStates') || [];
    const playerJoined = getStore('playerJoined');

    $: activeQuestion = $questions.find((q) => q.key === $activeEventData.activeQuestionKey);
    $: activeResponse = $responses.find((resp) => resp.key === $activeEventData.activeQuestionKey);
    $: questionState = $questionStates.find((qs) => qs.key === $activeEventData.activeQuestionKey);
    $: activeRoundState = $roundStates.find((rs) => rs.round_number === $activeEventData.activeRoundNumber);
    $: console.log(activeRoundState);

    $: hasImage = activeQuestion?.question_type.toLocaleLowerCase().startsWith('image');
    let displayLightbox = false;

    let responseText = '';
    $: notsubmitted = responseText && responseText !== activeResponse?.recorded_answer;
    const syncInputText = (e: Event) => {
        const target = <HTMLInputElement>e.target;
        responseText = target.value;
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
    {#if displayLightbox}
        <Lightbox source={activeQuestion?.question_url} on:click={() => (displayLightbox = false)} />
    {/if}
    <button class="button-image" on:click={() => (displayLightbox = true)}>
        <img src={activeQuestion?.question_url} alt="img round" />
    </button>
{:else if hasImage}
    <p>Image Missing</p>
{/if}

{#if activeRoundState?.scored}
    <div class="answer-summary">
        <p>Correct Answer: <strong>{activeQuestion?.display_answer}</strong></p>
        <!-- TODO multiply by megaround vals if appropriate, properly pluralize-->
        <p>You Received {activeResponse?.points_awarded || 0} pt(s) for this question</p>
        {#if activeResponse?.funny}
            <p>This answer was marked as a funny answer!</p>
        {/if}
    </div>
{/if}

<form on:submit|preventDefault={handleSubmitResponse}>
    <div id="response-container" class="input-container" class:notsubmitted>
        <input
            disabled={activeRoundState?.locked || !$playerJoined}
            required
            name="response_text"
            type="text"
            autocapitalize="none"
            autocorrect="off"
            autocomplete="off"
            spellcheck="false"
            value={activeResponse?.recorded_answer || ''}
            on:input={syncInputText}
        />
        <label for="response_text">Enter Answer</label>
    </div>

    {#if form?.error}<p>{form.error}</p>{/if}

    <button
        class:disabled={activeRoundState?.locked || !$playerJoined}
        class="button button-primary"
        disabled={activeRoundState?.locked || !$playerJoined}
    >
        Submit
    </button>
</form>

<style lang="scss">
    .question-text {
        padding: 0 0.5rem;
    }
    .answer-summary {
        max-width: var(--max-element-width);
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
