<script lang="ts">
    import { page } from '$app/stores';
    import { getStore, setEventCookie } from '$lib/utils';

    const joincode = $page.params.joincode;
    const rounds = getStore('rounds');
    const activeEventData = getStore('activeEventData');
    const currentEventData = getStore('currentEventData');

    const roundNumbers = $rounds.map((rd) => rd.round_number) || [];

    const handleRoundSelect = async (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;
        const postData = {
            activeQuestionNumber: 1,
            activeRoundNumber: Number(target.id),
            activeQuestionKey: `${target.id}.1`
        };
        $activeEventData = postData;
        setEventCookie($activeEventData, joincode);
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
