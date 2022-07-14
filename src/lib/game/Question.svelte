<script lang="ts">
    import { activeRound, activeQuestion} from '$stores/event'
    import Note from '$lib/Note.svelte'
	let currentResponse = ''; // TODO: check for an actual response
</script>

<h2>{$activeRound.round_number}.{$activeQuestion.question_number}</h2>

<p class="question-text">{$activeQuestion.text}</p>

<form on:submit|preventDefault>
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
