<script lang="ts">
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { getStore, setEventCookie } from '$lib/utils';

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

        setEventCookie($activeEventData, joincode);
        $page.url.pathname.endsWith('leaderboard') && goto(`/game/${joincode}`);
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
