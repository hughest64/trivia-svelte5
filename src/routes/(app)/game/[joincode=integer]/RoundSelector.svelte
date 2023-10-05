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

    const handleGotoQuestion = () => {
        $activeEventData = {
            activeQuestionNumber: $currentEventData.question_number,
            activeRoundNumber: $currentEventData.round_number,
            activeQuestionKey: $currentEventData.question_key
        };

        setEventCookie($activeEventData, joincode);
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

<button class="current-question-link" on:click={handleGotoQuestion}>
    go to current question {$currentEventData.question_key}
</button>

<style lang="scss">
    .current-question-link {
        text-decoration: underline;
    }
</style>
