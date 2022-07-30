<script lang="ts">
    // import { page } from '$app/stores';
    import { activeRound, } from '$stores/event';

    // const joinCode = $page.params?.joincode;
</script>

{#if !!$activeRound}
    <div class="container">
        {#each $activeRound?.questions as question (question.question_number)}
            <h3>Question {question.question_number}</h3>
            <p>{question.text}</p>
        {/each}
    </div>
{/if}

<style>
    .container {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        gap: 1em;
        margin-top: 1.5rem;
    }
</style>
