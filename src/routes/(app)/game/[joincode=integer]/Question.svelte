<script lang="ts">
    import { page }from '$app/stores';
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import type { ActionData } from './$types';
    import type { EventQuestion, Response, UserData } from '$lib/types';

    export let activeRoundQuestion: string;
    $: console.log('qustion', activeRoundQuestion);
    export let activeQuestion: EventQuestion;
    export let activeResponse: Response | undefined;
    $: console.log('ACTIVE RESPONSE!', activeResponse);

    $: form = <ActionData>$page.form;
    $: responseText = activeResponse?.recorded_answer || '';
    $: userData =  getStore<UserData>('userData');
    $: response = responseText;
    $: notsubmitted = false; // response && activeResponse?.recorded_answer !== response;
</script>

<h2>{activeRoundQuestion}</h2>

<p class="question-text">{activeQuestion.text}</p>

<!-- TODO: perhaps customizing enchance could help us reatiin the input after submitting and only for this r.q
or at least provide a spinner or some such -->
<form action="?/response" method="POST" use:enhance>
    <input type="hidden" name="team_id" value={$userData?.active_team_id || ''}>
    <input type="hidden" name="response_id" value={activeResponse?.id || ''}>
    <input type="hidden" name="key" value={activeRoundQuestion}>

    <div class="input-element" class:notsubmitted>
        <input required name="response_text" type="text" bind:value={response}>
        <label for="response_text">Enter Answer</label>
    </div>
    {#if form?.error}<p>{form.error}</p>{/if}
    <button class="button button-red">Submit</button>
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
</style>
