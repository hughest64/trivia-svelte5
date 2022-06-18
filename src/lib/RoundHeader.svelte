<script lang="ts">
    import { currentRoundNumber, currentQuestionNumber, roundNumbers } from '$stores/event'

    const handleRoundSelect = (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target
        currentRoundNumber.set(Number(target.id))
        // always reset the question when changing rounds
        currentQuestionNumber.set(1)
    }
    
</script>

<div class="container">
    {#each $roundNumbers as num}
        <button id="{String(num)}" on:click={handleRoundSelect}>{num}</button>
    {/each}
</div>

<style>
    .container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 1em;
    }
    button {
        padding: .5em .75em;
        font-size: 20px;
        cursor: pointer;
    }
</style>