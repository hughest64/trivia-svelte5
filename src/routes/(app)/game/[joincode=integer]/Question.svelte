<script lang="ts">
    import { getContext } from 'svelte';
    import { getStore } from '$lib/utils';
    import type { EventQuestion } from '$lib/types';

    export let activeRoundQuestion: string;
    export let activeQuestion: EventQuestion;

    const socket: WebSocket = getContext('socket');
    $: response = getStore('responseData');
    // $: console.log($response);

    const handleResponseSubmit = () => {
        socket.send(
            JSON.stringify({
                type: 'team.update_response',
                message: $response
            })
        );
    };
</script>

<h2>{activeRoundQuestion}</h2>

<p class="question-text">{activeQuestion.text}</p>

<form on:submit|preventDefault={handleResponseSubmit}>
    <div class="input-element">
        <input name="response" type="text" bind:value={$response} />
        <label for="response">Enter Answer</label>
    </div>
    <input class="button button-red" type="submit" value="Submit" />
</form>

<style lang="scss">
    h2 {
        margin: 0.5em;
    }
    .question-text {
        padding: 0 1em;
    }
</style>
