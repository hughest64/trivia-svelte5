<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { fade, fly, scale } from 'svelte/transition';
    import type { ActionData } from './$types';

    export let form: ActionData;
    let showContent = false;
    onMount(() => (showContent = true));
</script>

<svelte:head><title>Trivia Mafia | Welcome</title></svelte:head>

<main>
    {#if showContent}
        <div transition:fade|local={{ delay: 500, duration: 1000 }} class="demo-note flex-column">
            <h4>Welcome to the Trivia Mafia SvelteKit Demo!</h4>
            <a href="/about">Click for details</a>
        </div>
        <div transition:scale|local={{ duration: 1500 }} class="logo-container">
            <img src="TM2021-Flat-Stacked-WhiteBackground.svg" alt="Trivia Mafia" />
        </div>

        <div transition:fly|local={{ y: 500, duration: 1500 }} class="form-container flex-column">
            <a class="button button-primary" href={`/user/login${$page.url.search}`}> Login/Create Account </a>
            <form action="" method="POST">
                <input class="button button-tertiary" type="submit" value="Play as a Guest" />
            </form>
            {#if form?.error}<p>{form?.error}</p>{/if}
        </div>
    {/if}
</main>

<style lang="scss">
    main {
        padding-top: 0;
    }
    a {
        text-decoration: none;
    }
    .logo-container {
        margin-bottom: 4em;
        img {
            width: 30rem;
            margin: auto;
            display: block;
        }
    }
    .form-container {
        width: 100%;
    }
    .demo-note {
        padding: 1em;
        background-color: var(--color-primary);
        color: var(--color-tertiary);
        width: 100vw;
        h4 {
            margin-bottom: 0.5em;
        }
        a {
            color: var(--color-primry);
            text-decoration: underline;
            font-weight: bold;
        }
    }
</style>
