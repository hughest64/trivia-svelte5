<script lang="ts">
    import Correct from '$lib/leaderboards/icons/Correct.svelte';
    import HalfCredit from '$lib/leaderboards/icons/HalfCredit.svelte';
    import Wrong from '$lib/leaderboards/icons/Wrong.svelte';
    import type { ComponentType } from 'svelte';
    import type { ResponseMeta } from '$lib/types';

    // TODO: for players, clicking on a response navigates to that question in the event
    // points adjustment (probably a component)
    // tiebreaker stuffz

    export let roundResps: ResponseMeta[];

    const answerValueMap: Record<string, ComponentType> = {
        '0': Wrong,
        '0.5': HalfCredit,
        '1': Correct
    };
</script>

<ul class="response-group">
    {#each roundResps as response}
        {@const comp = answerValueMap[response.points_awarded]}
        <li class="response-container">
            <div>{response.key}</div>
            {#if comp}
                <svelte:component this={comp} />
            {:else}
                <div style:padding-left=".3rem">*</div>
            {/if}
            <div>{response.recorded_answer}</div>
            <div>{response.points_awarded}</div>
        </li>
    {/each}
</ul>

<style lang="scss">
    .response-group {
        padding: 0.5rem;
        div {
            padding: 0.25rem 0;
        }
        :last-child {
            justify-self: right;
        }
    }
    .response-container {
        display: grid;
        grid-template-columns: 30px 30px 1fr 1fr;
    }
</style>
