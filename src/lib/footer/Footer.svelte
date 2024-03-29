<script lang="ts">
    import { page } from '$app/stores';
    import { afterNavigate, replaceState } from '$app/navigation';
    import { getStore, setEventCookie, splitQuestionKey } from '$lib/utils';
    import GameIcon from '$lib/footer/icons/GameIcon.svelte';
    import ChatIcon from './icons/ChatIcon.svelte';
    import LeaderboardIcon from './icons/LeaderboardIcon.svelte';
    import MegaroundIcon from './icons/MegaroundIcon.svelte';
    import TeamIcon from './icons/TeamIcon.svelte';
    import ControlIcon from './icons/ControlIcon.svelte';
    import ScoringIcon from './icons/ScoringIcon.svelte';

    const reg = /^\/\(\w+\)\/(game|host)\/[[=\w]+]\/?/;
    const joinCode = $page.params?.joincode;

    $: routeId = $page.route.id?.split('/')[2];
    $: isEventRoute = reg.test($page.route.id || '');
    $: setActive = (link: string) => {
        const path = $page.url.pathname;
        return link === 'leaderboard' ? path.includes(link) : path.endsWith(link);
    };

    const activeEventData = getStore('activeEventData');
    const roundStates = getStore('roundStates');
    const setActiveQuestion = () => {
        // if all rounds are scored, do nothing
        const allRoundsAreScored = $roundStates.every((rs) => rs.locked);
        if (allRoundsAreScored) return;

        const minUnscoredRound = Math.min(...$roundStates.filter((rs) => !rs.scored).map((rs) => rs.round_number));
        $activeEventData = {
            activeRoundNumber: minUnscoredRound,
            activeQuestionNumber: 1,
            activeQuestionKey: `${minUnscoredRound}.1`
        };
        setEventCookie($activeEventData, $page.params.joincode);
    };

    afterNavigate(({ to }) => {
        const queryParams = to?.url.searchParams;
        const activeKey = queryParams?.get('active-key');
        // update the active question if provided
        if (activeKey && to?.url) {
            const { round, question } = splitQuestionKey(activeKey);
            $activeEventData = {
                activeRoundNumber: Number(round),
                activeQuestionNumber: Number(question),
                activeQuestionKey: activeKey
            };
            setEventCookie($activeEventData, joinCode);
            replaceState(`${to?.url.origin}${to?.url.pathname}`, {});
        }
    });
</script>

<nav>
    <ul id="nav-links" class:justify-nav={!isEventRoute}>
        {#if isEventRoute}
            <li class:active={setActive(joinCode)}>
                <a href={`/${routeId}/${joinCode}`}>
                    <GameIcon cls="svg" />
                    <p>Game</p>
                </a>
            </li>
            <li class:active={setActive('leaderboard')}>
                <a href={`/${routeId}/${joinCode}/leaderboard`}>
                    <LeaderboardIcon cls="svg" />
                    <p>Leaderboard</p>
                </a>
            </li>
        {/if}
        {#if routeId === 'game' && isEventRoute}
            <li class:active={setActive('chat')}>
                <a href={`/${routeId}/${joinCode}/chat`}>
                    <ChatIcon cls="svg" />
                    <p>Chat</p>
                </a>
            </li>
            <li class:active={setActive('megaround')}>
                <a href={`/game/${joinCode}/megaround`}>
                    <MegaroundIcon cls="svg" />
                    <p>Mega Round</p>
                </a>
            </li>
            <li class:active={setActive('score')}>
                <a data-sveltekit-reload href="/team/manage?prev={$page.url.pathname}">
                    <TeamIcon cls="svg" />
                    <p>Team</p>
                </a>
            </li>
        {:else if routeId === 'host' && isEventRoute}
            <li class:active={setActive('controlboard')}>
                <a href={`/${routeId}/${joinCode}/controlboard`}>
                    <ControlIcon cls="svg" />
                    <p>Controls</p>
                </a>
            </li>
            <li class:active={setActive('score')}>
                <a data-sveltekit-reload href={`/host/${joinCode}/score`} on:click={setActiveQuestion}>
                    <ScoringIcon cls="svg" />
                    <p>Scoring</p>
                </a>
            </li>
        {/if}
    </ul>
</nav>

<style lang="scss">
    nav {
        position: fixed;
        bottom: 0;
        width: 100%;
        font-size: 1.2em;
        z-index: 3;
    }
    ul {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin: 0 auto;
        padding: 0 0.75rem;
        width: 100%;
        max-width: var(--max-container-width);
        background-color: var(--color-tertiary);
    }
    li {
        padding: 0;
        margin: 0.25em 0;
    }

    /**.menu */
    li > a {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;
        width: 4.5rem;
        height: 4.5rem;
        margin: 0 auto;
        border: none;
        border-radius: 0.5em;
        text-decoration: none;
        color: var(--color-black);
        cursor: pointer;
    }
    a:hover,
    a:focus {
        text-decoration: none;
    }
    :global(.svg path) {
        fill: var(--color-alt-black);
        stroke: var(--color-alt-black);
    }
    p {
        font-size: 10px;
        margin: 0.25rem 0;
        color: var(--color-black);
    }
    .justify-nav {
        justify-content: flex-end;
    }
    .active {
        a {
            background-color: #413f43;
        }
        :global(.svg path),
        :global(.svg rect),
        :global(.svg circle) {
            fill: var(--color-text-white);
            stroke: var(--color-text-white);
        }
        p {
            color: var(--color-text-white);
        }
    }

    @media screen and (max-width: 600px) {
        ul {
            justify-content: space-around;
            padding: 0;
        }
    }
</style>
