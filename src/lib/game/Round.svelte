<script lang="ts">
    import { page } from '$app/stores'
	import Note from '$lib/Note.svelte';
	import {
		activeRound,
		activeRoundNumber,
		activeQuestion,
		activeQuestionNumber
	} from '$stores/event';

    const joinCode = $page.params?.joincode;
	let currentResponse = ''

	$: questionNumbers = $activeRound?.questions.map((q) => q.question_number);

	const handleQuestionSelect = async (event: MouseEvent) => {
		const target = <HTMLButtonElement>event.target;
		activeQuestionNumber.set(Number(target.id));
		// post to the game endpoint to set active round and question in a cookie
		await fetch(`/game/${joinCode}`, {
			method: 'POST',
			body: JSON.stringify({
				initialRoundNumber: $activeRoundNumber,
				initialQuestionNumber: target.id
			})
		});
	};
</script>

<div class="question-container flex-column">
	<div class="question-selector">
		{#each questionNumbers as num}
			<button class="button-white" id={String(num)} on:click={handleQuestionSelect}>{num}</button>
		{/each}
	</div>
	<div class="flex-column">
		<h2>{$activeRound.round_number}.{$activeQuestion.question_number}</h2>
		<p>{$activeQuestion.text}</p>
		<form on:click|preventDefault>
			<div class="input-element">
				<input name="response" type="text" bind:value={currentResponse} />
				<label for="response">Enter Answer</label>
			</div>
			<input class="button button-red" type="submt" value="Submit" />
		</form>
		<Note />
		
	</div>
</div>

<style lang="scss">
	.flex-column {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.question-container {
		border: 2px solid var(--color-black);
		border-radius: .5em;
		width: 50em;
		max-width: 96vw;
		margin: 1em;
		padding: 1em;
		box-shadow: 10px 0px 5px -5px rgb(0 0 0 / 80%);
		& > * {
			max-width: 100%;
		}
	}
	.question-selector {
		display: flex;
		gap: .5em;
		button {
			font-weight: bold;
			border: 2px solid var(--color-black);
		}
	}
	h2 {
		margin: .5em;
	}

</style>
