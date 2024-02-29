<!-- TODO: this seems like it will get busier so I think a component map like popups is in order
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
        <!-- TODO: a link back to the home page? -->
    {:else}
        <!-- <h1>Sorry</h1> -->
        <div class="limit-container">
            <p>
                Sorry! This game is limited to one device per team, and someone from your team has already joined this
                game.
            </p>
            <a class="button button-secondary" href="/team/create" data-sveltekit-reload>Go Here to create a new team</a
            >
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
    .limit-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        a {
            color: var(--color-tertiary);
            width: 18em;
            text-decoration: none;
        }
    }
</style>
