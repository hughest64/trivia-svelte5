<script lang="ts">
    import { dev } from '$app/environment';
    import { PUBLIC_API_HOST } from '$env/static/public';
    import { getStore } from './utils';
    import EventMeta from './EventMeta.svelte';
    import { linear } from 'svelte/easing';

    const userData = getStore('userData');
    $: userEmail = $userData.email;

    $: isHost = $userData.is_staff;
    const feedbackLink = `https://docs.google.com/forms/d/e/1FAIpQLSeT5FX2OGycY0yDqjiwj8ItAFi8CE64GatBiO-lsYAz1hLguA/viewform?usp=pp_url&entry.1807181492=${userEmail}`;

    const adminLink = dev ? `${PUBLIC_API_HOST}/admin` : '/admin';
</script>

<ul>
    <li><EventMeta /></li>
    <li><a href="/rules" on:click>Rules and FAQ</a></li>
    <li><a href="/user/settings" on:click data-sveltekit-reload>Manage Profile</a></li>
    <!-- <li>Manage Team</li> -->
    {#if isHost}
        <li><a href={adminLink} rel="external" on:click>Trivia Mafia Administration</a></li>
    {/if}
    <li><a href={feedbackLink} target="_blank" on:click>Submit App Feedback</a></li>
    {#if isHost}
        <li>
            <a href="https://hosts.triviamafia.com" rel="external" target="_blank" on:click>
                Trivia Mafia Host Feedback
            </a>
        </li>
    {/if}
    <li><a rel="external" href="/user/logout">Logout</a></li>
    <button on:click>X</button>
</ul>

<style lang="scss">
    ul {
        display: flex;
        flex-direction: column;
        height: 100%;
        margin: 1em;
        color: var(--color-tertiary);
        font-weight: bold;
    }
    li {
        margin: 1em 0;
        &:last-of-type {
            flex-grow: 1;
        }
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
