<script lang="ts">
    import { page } from '$app/stores';
    import { dev } from '$app/environment';
    import { PUBLIC_API_HOST } from '$env/static/public';
    import { getStore } from './utils';
    import AutoRevealToggle from './AutoRevealToggle.svelte';
    import EventMeta from './EventMeta.svelte';

    const joincode = $page.params.joincode;
    const prev = $page.url.pathname;

    const userData = getStore('userData');

    $: isGameEndpoint = $page.url.pathname.startsWith('/game');
    $: isHost = $userData.is_staff;
    $: feedbackQuery = !$userData.is_guest ? `?usp=pp_url&entry.1807181492=${$userData.email}` : '';
    $: feedbackLink = `https://docs.google.com/forms/d/e/1FAIpQLSeT5FX2OGycY0yDqjiwj8ItAFi8CE64GatBiO-lsYAz1hLguA/viewform${feedbackQuery}`;

    const adminLink = dev ? `${PUBLIC_API_HOST}/admin` : '/admin';
</script>

<ul>
    {#if joincode}
        <li><EventMeta /></li>
    {/if}

    {#if isGameEndpoint && joincode}
        <li>
            <form action="" class="auto-advance-form" on:submit|preventDefault>
                <span>Auto-Advance Questions</span>
                <AutoRevealToggle />
            </form>
        </li>
        <li><a href="/team/manage?prev={prev}" on:click data-sveltekit-reload>Team Page</a></li>
    {/if}

    <li><a href="/user/settings?prev={prev}" on:click data-sveltekit-reload>Manage Profile</a></li>
    <li><a href="/rules?prev={prev}" on:click data-sveltekit-reload>Rules and FAQ</a></li>

    {#if isHost}
        <li><a href={adminLink} rel="external" on:click>Trivia Mafia Administration</a></li>
    {/if}

    <li><a href={feedbackLink} target="_blank" on:click>Submit App Feedback</a></li>

    <li>
        <a href={isGameEndpoint ? '/game/join' : '/host/event-setup'} data-sveltekit-reload on:click>
            Join a Different Game
        </a>
    </li>

    <!-- {#if isHost}
        <li>
            <a href="https://hosts.triviamafia.com" rel="external" target="_blank" on:click>
                Trivia Mafia Host Feedback
            </a>
        </li>
    {/if} -->
    <li><a href={feedbackLink} target="_blank">Submit App Feedback</a></li>

    <li><a rel="external" href="/user/logout">Logout</a></li>
    <button on:click>X</button>
</ul>

<style lang="scss">
    ul {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        height: 100%;
        margin: 1em;
        color: var(--color-tertiary);
        font-weight: bold;
    }
    li {
        margin: 0;
        &:last-of-type {
            flex-grow: 1;
        }
    }
    .auto-advance-form {
        // outline: 1px dashed pink;
        position: relative;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        min-width: 100%;
    }
    a {
        text-decoration: none;
        color: var(--color-tertiary);
    }
    button {
        width: fit-content;
        text-align: right;
        align-self: flex-end;
        font-size: 2em;
        color: var(--color-tertiary);
        background-color: inherit;
        border: none;
        margin-bottom: 1em;
        cursor: pointer;
    }
</style>
