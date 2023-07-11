<script lang="ts">
    import type { Response } from '$lib/types';
    export let roundResps: Response[];
</script>

<ul>
    {#each roundResps as response}
        <li class="response-data">
            <span class="resp-key">{response.key}</span>
            <span>*</span>
            <span class="answer">{response.recorded_answer}</span>
            <span>{response.points_awarded}</span>
        </li>
    {/each}
</ul>

<style lang="scss">
    .response-data {
        display: flex;
        justify-content: start;
        gap: 1rem;
        span {
            margin: 0.2rem 0;
        }
    }
    .resp-key {
        width: 5%;
    }
    .answer {
        flex-grow: 1;
    }
</style>
