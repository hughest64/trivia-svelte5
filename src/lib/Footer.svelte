<script lang="ts">
    import { browser } from '$app/env';
    import { page } from '$app/stores';
    import QuizIcon from '$lib/icons/QuizIcon.svelte';
    import ChatIcon from './icons/ChatIcon.svelte';
    import LeaderboardIcon from './icons/LeaderboardIcon.svelte';
    import MegaroundIcon from './icons/MegaroundIcon.svelte';
    import MenuIcon from './icons/MenuIcon.svelte';
    import ScoringIcon from './icons/ScoringIcon.svelte';

    // example routes
    // const d = '(app)/host/[joincode=integer]'; // should match
    // const d2 = '(app)/game/join'; // should not match

    // TODO: better regex so we don't have to do multiple checks in isEventRoute
    const reg = /^\(\w+\)\/(game|host)\/[[=\w]+]\/?/;

    const joinCode = $page.params?.joincode;
    $: routeId = <string>$page.routeId?.split('/')[1];
    $: isEventRoute =
        reg.test($page.routeId || '') && $page.routeId !== '(app)/game/join' && $page.routeId !== '(app)/host/event-setup';

    $: isActive = (id: string) => {
        if (!browser) return false;
        const link = <HTMLAnchorElement>document.querySelector(id)?.firstChild;
        const linkHref = link?.href;

        return linkHref === $page.url.href;
    };
</script>

<nav>
    <ul id="nav-links" class:justify-nav={!isEventRoute}>
        {#if isEventRoute}
            <li id="quiz" class:active={isActive('#quiz')}>
                <a href={`/${routeId}/${joinCode}`}>
                    <div>
                        <QuizIcon class="svg" />
                        <p>Quiz</p>
                    </div>
                </a>
            </li>
            <li id="leaderboard" class:active={isActive('#leaderboard')}>
                <a href={`/${routeId}/${joinCode}/leaderboard`}>
                    <div>
                        <LeaderboardIcon class="svg" />
                        <p>Leaderboard</p>
                    </div>
                </a>
            </li>
            <li id="chat" class:active={isActive('#chat')}>
                <a href={`/${routeId}/${joinCode}/chat`}>
                    <div>
                        <ChatIcon class="svg" />
                        <p>Chat</p>
                    </div>
                </a>
            </li>
        {/if}
        {#if routeId === 'game' && isEventRoute}
            <li id="megaround" class:active={isActive('#megaround')}>
                <a href={`/game/${joinCode}/megaround`}>
                    <div>
                        <MegaroundIcon class="svg" />
                        <p>Megaround</p>
                    </div>
                </a>
            </li>
        {:else if routeId === 'host' && isEventRoute}
            <li id="score" class:active={isActive('#score')}>
                <a href={`/host/${joinCode}/score`}>
                    <div>
                        <ScoringIcon class="svg" />
                        <p>Scoring</p>
                    </div>
                </a>
            </li>
        {/if}
        <li>
            <div on:click>
                <MenuIcon class="svg" />
                <p>Menu</p>
            </div>
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
    li > a {
        text-decoration: none;
    }
    div {
        width: 4em;
        height: 4em;
        background-color: #fcfcfc;
        border-radius: 0.5em;
        margin: auto;
        padding: 0.25em;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
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
        div {
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
</style>
