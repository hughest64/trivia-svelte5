<script lang="ts">
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { getStore, setEventCookie } from '$lib/utils';

    const rounds = getStore('rounds');
    const roundNumbers = $rounds?.map((rd) => rd.round_number) || [];
    const roundStates = getStore('roundStates');
    const responses = getStore('responseData');
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
        const pathname = $page.url.pathname;

        if (pathname.endsWith('leaderboard') || pathname.endsWith('summary')) {
            goto(`/game/${joincode}`);
        }
    };

    $: missingResponses = (roundNumber: number) => {
        if ($currentEventData.round_number <= roundNumber) return false;

        const roundIsLocked = $roundStates.find((rs) => rs.round_number === roundNumber && rs.locked);
        if (roundIsLocked) return false;

        const round = $rounds.find((r) => r.round_number === roundNumber);
        const roundResponseCount = $responses.filter((resp) => resp.round_number === roundNumber).length || 0;
        // all questions have been answered
        if (round?.question_count === roundResponseCount) return false;

        return true;
    };
    $: roundIsLocked = (roundNumber: Number) => {
        return !!$roundStates.find((rs) => rs.round_number === roundNumber && rs.locked);
    };
</script>

<div class="round-selector">
    {#each roundNumbers as roundNum}
        <button
            class:active={$activeEventData.activeRoundNumber === roundNum}
            class:current={$currentEventData.round_number === roundNum}
            class:unresponded={missingResponses(roundNum)}
            class:roundlocked={roundIsLocked(roundNum)}
            id={String(roundNum)}
            on:click={handleRoundSelect}
        >
            {roundNum}
        </button>
    {/each}
</div>

<style lang="scss">
    button {
        position: relative;
        &.roundlocked {
            position: relative;
            background-image: url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20viewBox%3D%220%200%2033.073%2033.073%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%3E%3Cg%20transform%3D%22matrix(1.00296%200%200%201.00296%20-.049%20-.043)%22%3E%3Crect%20width%3D%2221.104%22%20height%3D%2216.01%22%20x%3D%225.984%22%20y%3D%2214.417%22%20ry%3D%222.443%22%20fill%3D%22%23413f43%22%20fill-rule%3D%22evenodd%22%2F%3E%3Cpath%20d%3D%22M5.984%2027.984v.001c0%20.368.081.715.225%201.027h20.655c.144-.312.225-.66.225-1.027v-.001z%22%20fill%3D%22%23dc0926%22%20fill-rule%3D%22evenodd%22%2F%3E%3Cg%20transform%3D%22matrix(.2911%200%200%20.2911%20-63.608%20-12.386)%22%20fill%3D%22%23dc0926%22%3E%3Ccircle%20cx%3D%22275.324%22%20cy%3D%22117.241%22%20r%3D%226.25%22%2F%3E%3Cpath%20d%3D%22M271.337%20115.843h7.974v12.321h-7.974z%22%2F%3E%3C%2Fg%3E%3C%2Fg%3E%3Cpath%20d%3D%22M16.536%207.027a5.953%205.953%200%2000-5.953%205.953v5.945h2.707v-6.088h.008a3.247%203.247%200%20013.238-3.104%203.247%203.247%200%20013.244%203.104h.004V14.727h2.706V12.98a5.953%205.953%200%2000-5.954-5.953z%22%20fill%3D%22%23413f43%22%20fill-rule%3D%22evenodd%22%2F%3E%3C%2Fsvg%3E');
            background-repeat: no-repeat;
            background-size: 35% 35%;
        }
        &.unresponded {
            &::after {
                position: absolute;
                content: '!';
                top: 0;
                right: 0.15rem;
            }
        }
    }
</style>
