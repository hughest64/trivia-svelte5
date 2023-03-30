<script lang="ts">
    import { page } from '$app/stores';
    // import { goto } from '$app/navigation';
    import { getStore } from '$lib/utils';

    const joincode = $page.params.joincode;
    const rounds = getStore('rounds');
    const roundStates = getStore('roundStates');
    const activeEventData = getStore('activeEventData');
    const currentEventData = getStore('currentEventData');

    const roundNumbers = $rounds.map((rd) => rd.round_number) || [];
    $: isScoringPage = $page.url.pathname.includes('score');

    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;
        const postData = {
            activeQuestionNumber: 1,
            activeRoundNumber: Number(target.id),
            activeQuestionKey: `${target.id}.1`
        };
        $activeEventData = postData;

        // post to the game endpoint to set active round and question in a cookie
        await fetch('/update', {
            method: 'POST',
            body: JSON.stringify({ activeEventData: postData, joincode: joincode })
        });
    };
</script>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        {#if !isScoringPage || !!$roundStates.find((rd) => rd.round_number === roundNum)?.locked}
            <button
                id={String(roundNum)}
                on:click={handleRoundSelect}
                class:active={$activeEventData.activeRoundNumber === roundNum}
                class:current={$currentEventData.round_number === roundNum}
            >
                {roundNum}
            </button>
        {/if}
    {/each}
</div>
