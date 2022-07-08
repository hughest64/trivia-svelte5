<script lang="ts">
	import { fly } from 'svelte/transition';
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
	$: roundQuestions = $activeRound?.questions;
	let xValue = 500;

	const handleQuestionSelect = async (event: MouseEvent) => {
		const target = <HTMLButtonElement>event.target;
		const nextQuestionNumber = Number(target.id)
		xValue = nextQuestionNumber < $activeQuestionNumber ? Math.abs(xValue) : Math.abs(xValue) * -1
		activeQuestionNumber.set(nextQuestionNumber);
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
	<div class="another-container">
	{#each roundQuestions as question (question.question_number)}
	{#if question.question_number === $activeQuestionNumber}
	<!-- out:fly={{x: xValue, duration: 600, opacity: 100}} -->
	<div
		class="flex-column question"
		in:fly={{x: xValue, duration: 600, opacity: 100}}
	>
		<h2>{$activeRound.round_number}.{question.question_number}</h2>
		<p>{question.text}</p>
		<form on:click|preventDefault>
			<div class="input-element">
				<input name="response" type="text" bind:value={currentResponse} />
				<label for="response">Enter Answer</label>
			</div>
			<input class="button button-red" type="submt" value="Submit" />
		</form>
		<Note />
		
	</div>
	{/if}
	{/each}
</div>
</div>

<style lang="scss">
	.another-container {
		display: flex;
	}
	.flex-column {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.question-container {
		overflow-x: hidden;
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
