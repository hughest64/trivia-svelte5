<script lang="ts">
    export let roundNumbers: (string | number)[] = []
    
</script>

<div class="container">
    {#each roundNumbers as num}
        <button>{num}</button>
    {/each}
</div>

<style>
    .container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 1em;
        /* max-width: 30rem; */
        /* margin: 5rem auto 0; */
    }
    button {
        padding: .5em .75em;
        font-size: 20px;
        cursor: pointer;
    }
</style>