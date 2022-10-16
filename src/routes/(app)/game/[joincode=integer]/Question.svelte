<script lang="ts">
    // import { getContext } from 'svelte';
    import { enhance } from '$app/forms';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import type { ActionData } from './$types';
    import type { EventQuestion } from '$lib/types';

    export let form: ActionData;
    export let activeRoundQuestion: string;
    export let activeQuestion: EventQuestion;

    $: userData = $page.data?.user_data;
    // const socket: WebSocket = getContext('socket');
    $: responseStore = getStore('responseData');
    $: response = $responseStore; // filtered to this r.q
    $: notsubmitted = $responseStore !== response;

    // const handleResponseSubmit = () => {
    // or - we could just use client fetch here
    //     socket.send(
    //         JSON.stringify({
    //             type: 'team.update_response',
    //             message: response
    //         })
    //     );
    // };
</script>

<h2>{activeRoundQuestion}</h2>

<p class="question-text">{activeQuestion.text}</p>

<!-- <form on:submit|preventDefault={handleResponseSubmit}> -->
<!-- <form action="/response" method="post" use:enhance={({ data }) => {
    data.set('round_question', activeRoundQuestion);
    data.set('team_id', String(userData?.active_team_id || ''));
}}> -->
<form action="/response" method="post" use:enhance>
    {#if form?.error}<p>{form.error}</p>{/if}
    <!-- <input type="hidden" name="team_id" value={userData?.active_team_id}>
    <input type="hidden" name="round_question" value={activeRoundQuestion}> -->
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
