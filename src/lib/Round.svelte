<script lang="ts">
    import { currentRound, currentQuestion, currentQuestionNumber } from '$stores/event';

    $: questionNumbers = $currentRound?.questions.map(q => q.question_number)

    const handleQuestionSelect = (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target
        currentQuestionNumber.set(Number(target.id))

    }
</script>

<div class="container">
    {#each questionNumbers as num }
        <button id={String(num)} on:click={handleQuestionSelect}>{num}</button>
    {/each}
</div>
<div>
    <h3>R {$currentRound.round_number} Q {$currentQuestion.question_number}</h3>
    <p>{$currentQuestion.text}</p>
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
        padding: .5em .75em;
        font-size: 16px;
        font-weight: bold;
        border: none;
        background-color: inherit;
        cursor: pointer;
    }
</style>