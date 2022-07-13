<script lang="ts">
	import { fade, fly, slide } from 'svelte/transition';
	import { sineIn, sineInOut, sineOut } from 'svelte/easing'
	import { page } from '$app/stores';
	import Note from '$lib/Note.svelte';
	import { swipeQuestion } from './swipe';
	import {
		activeRound,
		activeRoundNumber,
		activeQuestion,
		activeQuestionNumber
	} from '$stores/event';

	const joinCode = $page.params?.joincode;
	let currentResponse = ''; // TODO: this will actually tie to a response

	$: questionNumbers = $activeRound?.questions.map((q) => q.question_number);
	$: lastQuestionNumber = Math.max(...questionNumbers)

	let swipeDirection = 'right'; // or 'left'
	$: swipeXValue = swipeDirection === 'right' ? 1000 : -4000;

	const inSwipeDuration = 600
	const outSwipeDuration = 350

	const handleQuestionSelect = async (event: MouseEvent|CustomEvent|KeyboardEvent) => {
		const target = <HTMLElement>event.target;
		const eventDirection = event.detail?.direction;
		let nextQuestionNumber = $activeQuestionNumber;

		if (eventDirection === 'right' || (event as KeyboardEvent).code === 'ArrowRight') {
			nextQuestionNumber = Math.min(lastQuestionNumber, $activeQuestionNumber + 1);
		} else if (eventDirection === 'left' || (event as KeyboardEvent).code === 'ArrowLeft') {
			nextQuestionNumber = Math.max(1, $activeQuestionNumber - 1);
		} else if (!!target.id) {
			nextQuestionNumber = Number(target.id);
		}

		swipeDirection = nextQuestionNumber < $activeQuestionNumber ? 'left' : 'right';
		activeQuestionNumber.set(nextQuestionNumber);

		// post to the game endpoint to set active round and question in a cookie
		await fetch(`/game/${joinCode}`, {
			method: 'POST',
			body: JSON.stringify({
				initialRoundNumber: $activeRoundNumber,
				initialQuestionNumber: $activeQuestionNumber
			})
		});
	};
</script>

<svelte:window on:keyup={handleQuestionSelect} />

<div class="question-box flex-column">
	<div class="question-selector">
		{#each questionNumbers as num}
			<button class="button-white" id={String(num)} on:click={handleQuestionSelect}>{num}</button>
		{/each}
	</div>
	<div class="all-questions">
	{#key $activeQuestionNumber}
		<div
			class="flex-column"
			in:fly={{ easing: sineInOut, opacity: 100, x: swipeXValue, duration: inSwipeDuration }}
			out:fly={{ easing: sineInOut, opacity: 100, x: swipeXValue * -1, duration: outSwipeDuration }}
			use:swipeQuestion
			on:swipe={handleQuestionSelect}
		>
			<h2>{$activeRound.round_number}.{$activeQuestion.question_number}</h2>
			<p>{$activeQuestion.text}</p>
			<form on:submit|preventDefault>
				<div class="input-element">
					<input name="response" type="text" bind:value={currentResponse} />
					<label for="response">Enter Answer</label>
				</div>
				<input class="button button-red" type="submit" value="Submit" />
			</form>
			<Note />
		</div>
	{/key}
	</div>
</div>

<style lang="scss">
	.all-questions {
		display: flex;
		// flex-direction: row;
		& > * {
			max-width: 100%;
		}
	}
	.flex-column {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	.question-box {
		overflow-x: hidden;
		border: 2px solid var(--color-black);
		border-radius: 0.5em;
		width: 50em;
		max-width: calc(100% - 2em);
		margin-top: 1em;
		padding-top: 1em;
		box-shadow: 10px 0px 5px -5px rgb(0 0 0 / 80%);
		& > * {
			max-width: 100%;
		}
	}
	.question-selector {
		display: flex;
		gap: 0.5em;
		button {
			font-weight: bold;
			border: 2px solid var(--color-black);
		}
	}
	h2 {
		margin: 0.5em;
	}
</style>
