<script lang="ts">
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { getStore } from '$lib/utils';

    const rounds = getStore('rounds');
    const roundNumbers = $rounds?.map((rd) => rd.round_number) || [];
    const activeEventData = getStore('activeEventData');
    const currentEventData = getStore('currentEventData');
    $: joincode = $page.params?.joincode;

    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;

        $activeEventData = {
            activeQuestionNumber: 1,
            activeRoundNumber: Number(target.id),
            activeQuestionKey: `${target.id}.1`
        };

        // post to the game endpoint to set active round and question in a cookie
        await fetch('/update', {
            method: 'POST',
            body: JSON.stringify({ activeEventData: $activeEventData, joincode })
        }).then(() => {
            $page.url.pathname.endsWith('leaderboard') && goto(`/game/${joincode}`);
        });
    };
</script>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        <button
            class:active={$activeEventData.activeRoundNumber === roundNum}
            class:current={$currentEventData.round_number === roundNum}
            id={String(roundNum)}
            on:click={handleRoundSelect}
        >
            {roundNum}
        </button>
    {/each}
</div>
