<script lang="ts">
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { getStore } from '$lib/utils';
    import type { ActiveEventData, CurrentEventData } from '$lib/types';

    const roundNumbers = $page.data.rounds?.map((rd) => rd.round_number) || [];
    const joincode = $page.params.joincode;
    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: currentEventData = getStore<CurrentEventData>('currentEventData');

    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;
        const willNavigate = $page.url.pathname.includes('score');
        const postData = {
            activeQuestionNumber: 1,
            activeRoundNumber: Number(target.id),
            activeQuestionKey: `1.${target.id}`
        };
        if (!willNavigate) $activeEventData = postData;

        // post to the game endpoint to set active round and question in a cookie
        await fetch('/update', {
            method: 'POST',
            body: JSON.stringify({ activeEventData: postData, joincode: joincode })
        });
        willNavigate && goto(`/host/${joincode}/score/${target.id}`);
    };
</script>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        <button
            id={String(roundNum)}
            on:click={handleRoundSelect}
            class:active={$activeEventData.activeRoundNumber === roundNum}
            class:current={$currentEventData.round_number === roundNum}
        >
            {roundNum}
        </button>
    {/each}
</div>
