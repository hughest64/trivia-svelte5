<script lang="ts">
    import { page } from '$app/stores'
    import { activeRoundNumber, activeQuestionNumber, roundNumbers } from '$stores/event'
  
    const joinCode = $page.params?.joincode;

    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target
        activeRoundNumber.set(Number(target.id))
        // always reset the question when changing rounds
        activeQuestionNumber.set(1)
        // post to the game endpoint to set active round and question in a cookie
        // await fetch(`/game/${joinCode}`, {
        //     method: 'POST',
        //     body: JSON.stringify({
        //         initialRoundNumber: target.id,
        //         initialQuestionNumber: 1
        //     })
        // })
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