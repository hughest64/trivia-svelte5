<script lang="ts">
    import { page } from '$app/stores';
    import type { ActionData } from './$types';

    export let form: ActionData;
</script>

<svelte:head><title>Trivia Mafia | Welcome</title></svelte:head>

<main>
    <div class="logo-container">
        <img src="TM2021-Flat-Stacked-WhiteBackground.svg" alt="Trivia Mafia" />
    </div>

    {#if form?.error}<p>{form?.error}</p>{/if}

    <a class="button button-red" href={`/user/login${$page.url.search}`}> Login/Create Account </a>
    <!-- TODO: button with a formAction? -->
    <form action="" method="POST">
        <input class="button button-white" type="submit" value="Play as a Guest">
    </form>
</main>

<style lang="scss">
    a {
        text-decoration: none;
    }
    .logo-container {
        margin-bottom: 4em;
        img {
            width: 30em;
            max-width: calc(100% - 2em);
            margin: auto;
            display: block;
        }
    }
</style>
