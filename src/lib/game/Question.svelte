<script lang="ts">
    import { activeRound, activeQuestion } from '$stores/event';
    import { socket } from '$stores/socket';
    import { response } from '$stores/response';
    import Note from './Note.svelte';

    $: currentResponse = $response; // TODO: check for an actual response

    const handleResponseSubmit = () => {
        $socket.send(
            JSON.stringify({
                type: 'team.update_response',
                message: { reponse: currentResponse }
            })
        );
    };
</script>

<h2>{$activeRound.round_number}.{$activeQuestion.question_number}</h2>

<p class="question-text">{$activeQuestion.text}</p>

<form on:submit|preventDefault={handleResponseSubmit}>
    <div class="input-element">
        <input name="response" type="text" bind:value={currentResponse} />
        <label for="response">Enter Answer</label>
    </div>
    <input class="button button-red" type="submit" value="Submit" />
</form>

<Note />

<style lang="scss">
    h2 {
        margin: 0.5em;
    }
    .question-text {
        padding: 0 1em;
    }
</style>
