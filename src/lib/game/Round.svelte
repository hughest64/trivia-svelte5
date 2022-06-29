<script lang="ts">
    import { page } from '$app/stores'
	import {
		activeRound,
		activeRoundNumber,
		activeQuestion,
		activeQuestionNumber
	} from '$stores/event';

    const joinCode = $page.params?.joincode;

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

<div class="container">
	{#each questionNumbers as num}
		<button id={String(num)} on:click={handleQuestionSelect}>{num}</button>
	{/each}
</div>
<div>
	<h3>R {$activeRound.round_number} Q {$activeQuestion.question_number}</h3>
	<p>{$activeQuestion.text}</p>
</div>

<style>
	.container {
		display: flex;
		flex-direction: row;
		justify-content: center;
		gap: 1em;
		margin-top: 1.5rem;
	}
	button {
		padding: 0.5em 0.75em;
		font-size: 16px;
		font-weight: bold;
		border: none;
		background-color: inherit;
		cursor: pointer;
	}
</style>
