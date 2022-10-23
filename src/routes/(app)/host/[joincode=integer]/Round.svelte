<script lang="ts">
    // import { page } from '$app/stores';
    import type { EventRound } from '$lib/types';

    // const joinCode = $page.params?.joincode;
    export let activeRound: EventRound;
</script>

<!-- TODO: container with the reveal all stuffz -->
<h4>{activeRound.title}</h4>

{#each activeRound?.questions as question (question.question_number)}
    <h3>Question {question.question_number}</h3>
    <p>{question.text}</p>
{/each}

<style>

    h4 {
        margin: 2em 0.25em;
    }
</style>
