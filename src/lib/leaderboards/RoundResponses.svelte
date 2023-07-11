<script lang="ts">
    import type { Response } from '$lib/types';
    export let roundResps: Response[];
</script>

<ul class="response-group">
    {#each roundResps as response}
        <li class="response-container">
            <div class="response-item">{response.key}</div>
            <div class="response-item">*</div>
            <div class="response-item">{response.recorded_answer}</div>
            <div class="last-item">{response.points_awarded}</div>
        </li>
    {/each}
</ul>

<style lang="scss">
    .response-group {
        padding: 0.5rem;
    }
    .response-container {
        display: grid;
        grid-template-columns: 35px 25px 1fr 1fr;
        // gap: 0.5rem;
        .response-item {
            align-self: center;
            padding: 0.1rem 0;
        }
        .last-item {
            justify-self: right;
        }
    }
</style>
