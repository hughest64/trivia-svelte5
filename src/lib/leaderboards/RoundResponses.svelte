<script lang="ts">
    import Correct from '$lib/leaderboards/icons/Correct.svelte';
    import HalfCredit from '$lib/leaderboards/icons/HalfCredit.svelte';
    import Wrong from '$lib/leaderboards/icons/Wrong.svelte';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { getStore, setEventCookie, splitQuestionKey } from '$lib/utils';
    import type { ComponentType } from 'svelte';
    import type { ResponseMeta } from '$lib/types';

    // TODO:
    // points adjustment (probably a component)
    // tiebreaker stuffz

    export let roundResps: ResponseMeta[];
    const activeEventData = getStore('activeEventData');

    const answerValueMap: Record<string, ComponentType> = {
        '0': Wrong,
        '0.5': HalfCredit,
        '1': Correct
    };

    const gotoQuestion = async (response: ResponseMeta) => {
        if ($page.url.pathname.startsWith('/host')) return;
        const { round, question } = splitQuestionKey(response.key);
        const joincode = $page.params.joincode;
        $activeEventData = {
            activeQuestionKey: response.key,
            activeRoundNumber: Number(round),
            activeQuestionNumber: Number(question)
        };
        setEventCookie($activeEventData, joincode);
        goto(`/game/${joincode}`);
    };
</script>

<ul class="response-group">
    {#each roundResps as response}
        {@const comp = answerValueMap[response.points_awarded]}
        <li>
            <button class="response-container" on:click={() => gotoQuestion(response)}>
                <div>{response.key}</div>
                {#if comp}
                    <svelte:component this={comp} />
                {:else}
                    <div style:padding-left=".3rem">-</div>
                {/if}
                <div>{response.recorded_answer}</div>
                <div>{response.points_awarded}</div>
            </button>
        </li>
    {/each}
</ul>

<style lang="scss">
    .response-group {
        padding: 0.5rem;
        div {
            padding: 0.25rem 0;
        }
    }
    .response-container {
        display: grid;
        grid-template-columns: 30px 30px 3fr 1fr;
        width: 100%;
        text-align: left;
        font-size: 1rem;
        padding: 0;
        div {
            color: var(--color-secondary);
        }
        :last-child {
            justify-self: right;
        }
    }
</style>
