<!-- TODO: this seems like it will get busier so I think a compoenent map like popups is in order
i.e. handle different errors in separate svelte components and use the code (if present) to map
a component form an object (or acutal map) -->
<script lang="ts">
    import { page } from '$app/stores';

    $: code = $page.error?.code;
</script>

<main class="error-page">
    {#if !code}
        <h1>{$page.status}</h1>
        <h5>{$page.error?.message}</h5>
    {:else}
        <h1>Sorry</h1>
        <p>The player limit for your team has been reached for this event</p>
        <div class="button-container">
            <a class="button button-black" href="/game/join">Join a Different Game</a>
            <a class="button button-red" href="/team">Select a Different Team</a>
        </div>
    {/if}
    {#if $page.error?.next && !$page.url.pathname.includes('host')}
        <p>click <a rel="external" href={$page.error.next}>here</a> to try again</p>
    {/if}
</main>

<style lang="scss">
    main {
        max-width: calc(100% - 2em);
        margin: auto 1em;
    }
    .button-container {
        display: flex;
        flex-direction: column;
        a {
            width: 18em;
            text-decoration: none;
        }
    }
</style>
