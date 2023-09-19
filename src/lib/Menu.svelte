<script lang="ts">
    import { page } from '$app/stores';
    import { dev } from '$app/environment';
    import { PUBLIC_API_HOST } from '$env/static/public';

    $: isHostEndpoint = $page.url.pathname.startsWith('/host');

    const adminLink = dev ? `${PUBLIC_API_HOST}/admin` : '/admin';
</script>

<ul>
    <li><a href="/rules" on:click>Rules and FAQ</a></li>
    <li><a href="/user/settings" on:click data-sveltekit-reload>Manage Profile</a></li>
    <!-- <li>Manage Team</li> -->
    <li><a href={adminLink} rel="external" on:click>Trivia Mafia Administration</a></li>
    <li>Submit App Feedback</li>
    {#if isHostEndpoint}
        <li><a href="https://hosts.triviamafia.com" rel="external" target="_blank">Trivia Mafia Host Feedback</a></li>
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
