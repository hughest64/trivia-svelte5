<script lang="ts">
    import { enhance } from '$app/forms';
    import { page } from '$app/stores';
    import type { ActionData } from './$types';
    import type { EventQuestion, Response } from '$lib/types';

    export let form: ActionData = {};
    export let activeRoundQuestion: string;
    export let activeQuestion: EventQuestion;
    export let activeResponse: Response | undefined;
    $: responseText = activeResponse?.recorded_answer || '';

    $: userData = $page.data?.user_data;
    $: response = responseText;
    $: notsubmitted = response && activeResponse?.recorded_answer !== response;
</script>

<h2>{activeRoundQuestion}</h2>

<p class="question-text">{activeQuestion.text}</p>

<!-- TODO: client fetch maybe a better answer here, w/o use:enhance we refreshing the page on each submission
     (i.e. disconnect, reconnect to the socket) and with it we lose our state (userData.active_team_id, etc)
     if might be fine as long as the response always return user data, but it seems like risky overhead to me
-->
<form action="?/response" method="post" use:enhance>
    {#if form?.error}<p>{form.error}</p>{/if}

    <input type="hidden" name="team_id" value={userData?.active_team_id}>
    <input type="hidden" name="round_question" value={activeResponse?.key}>
    <input type="hidden" name="response_id" value={activeResponse?.id || ''}>

    <div class="input-element" class:notsubmitted >
        <input name="response_text" type="text" bind:value={response} />
        <label for="response_text">Enter Answer</label>
    </div>

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
