<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import QuizIcon from '$lib/footer/icons/QuizIcon.svelte';
    import ChatIcon from './icons/ChatIcon.svelte';
    import LeaderboardIcon from './icons/LeaderboardIcon.svelte';
    import MegaroundIcon from './icons/MegaroundIcon.svelte';
    import MenuIcon from './icons/MenuIcon.svelte';
    import ScoringIcon from './icons/ScoringIcon.svelte';
    import type { ActiveEventData } from '$lib/types';

    $: activeEventData = getStore<ActiveEventData>('activeEventData');

    const reg = /^\/\(\w+\)\/(game|host)\/[[=\w]+]\/?/;
    const joinCode = $page.params?.joincode;

    $: routeId = $page.route.id?.split('/')[2];
    $: isEventRoute = reg.test($page.route.id || '');
    $: setActive = (link: string) => $page.url.pathname.endsWith(link);
</script>

<nav>
    <ul id="nav-links" class:justify-nav={!isEventRoute}>
        {#if isEventRoute}
            <li class:active={setActive(joinCode)}>
                <a data-sveltekit-preload-data="tap" href={`/${routeId}/${joinCode}`}>
                    <QuizIcon cls="svg" />
                    <p>Quiz</p>
                </a>
            </li>
            <li class:active={setActive('leaderboard')}>
                <a data-sveltekit-preload-data="tap" href={`/${routeId}/${joinCode}/leaderboard`}>
                    <LeaderboardIcon cls="svg" />
                    <p>Leaderboard</p>
                </a>
            </li>
            <li class:active={setActive('chat')}>
                <a data-sveltekit-preload-data="tap" href={`/${routeId}/${joinCode}/chat`}>
                    <ChatIcon cls="svg" />
                    <p>Chat</p>
                </a>
            </li>
        {/if}
        {#if routeId === 'game' && isEventRoute}
            <li class:active={setActive('megaround')}>
                <a data-sveltekit-preload-data="tap" href={`/game/${joinCode}/megaround`}>
                    <MegaroundIcon cls="svg" />
                    <p>Megaround</p>
                </a>
            </li>
        {:else if routeId === 'host' && isEventRoute}
            <li class:active={setActive($page.params.round ? `score/${$page.params.round}` : 'score')}>
                <a
                    data-sveltekit-preload-data="tap"
                    href={`/host/${joinCode}/score/${$activeEventData.activeRoundNumber || 1}`}
                >
                    <ScoringIcon cls="svg" />
                    <p>Scoring</p>
                </a>
            </li>
        {/if}
        <li>
            <button class="menu" on:click>
                <MenuIcon cls="svg" />
                <p>Menu</p>
            </button>
        </li>
    </ul>
</nav>

<style lang="scss">
    nav {
        font-size: 1.2em;
    }
    ul {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin: 0 auto;
        max-width: calc(100% - 2em);
    }
    li {
        padding: 0;
        margin: 0.25em 0;
    }

    li > a,
    .menu {
        text-decoration: none;
        width: 4em;
        height: 4em;
        background-color: #fcfcfc;
        border-radius: 0.5em;
        margin: 0 auto;
        padding: 0.5em;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .menu {
        margin: 0;
        padding: 0;
        border: none;
    }
    a:hover,
    a:focus {
        text-decoration: none;
    }
    :global(.svg path) {
        fill: #413f43;
        stroke: #413f43;
        // &:not(.no-color-change) path {
        // fill: #413f43;
        // stroke: #413f43;
        // }
    }
    p {
        font-size: 10px;
        margin: 5px 0;
        color: var(--color-black);
    }
    .justify-nav {
        justify-content: flex-end;
        // margin: 0.5em;
    }
    .active {
        a {
            background-color: #413f43;
        }
        :global(.svg path) {
            fill: #fcfcfc;
            stroke: #fcfcfc;
        }
        // svg:not(.no-color-change) path {
        // 	fill: #fcfcfc;
        // 	stroke: #fcfcfc;
        // }
        p {
            color: #fcfcfc;
        }
    }
    .menu {
        cursor: pointer;
    }
</style>
