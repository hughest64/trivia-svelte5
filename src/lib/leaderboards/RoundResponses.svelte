<script lang="ts">
    import Correct from '$lib/icons/Correct.svelte';
    import type { ResponseMeta } from '$lib/types';

    export let roundResps: ResponseMeta[];
</script>

<ul class="response-group">
    {#each roundResps as response}
        <li class="response-container">
            <div>{response.key}</div>
            <Correct />
            <div>{response.recorded_answer}</div>
            <div>{response.points_awarded}</div>
        </li>
    {/each}
</ul>

<style lang="scss">
    .response-group {
        padding: 0.5rem;
        div {
            padding: 0.1rem 0;
        }
        :last-child {
            justify-self: right;
        }
    }
    .response-container {
        display: grid;
        grid-template-columns: 35px 25px 1fr 1fr;
    }
</style>
