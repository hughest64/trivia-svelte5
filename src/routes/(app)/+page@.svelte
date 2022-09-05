<script lang="ts">
    import { page } from '$app/stores';
    import type { Errors } from './$types';

    export let errors: Errors;
</script>

<svelte:head><title>Trivia Mafia | Welcome</title></svelte:head>

<div class="logo-container">
    <img src="TM2021-Flat-Stacked-WhiteBackground.svg" alt="Trivia Mafia" />
</div>

{#if errors?.message}<p>{errors?.message}</p>{/if}

<a class="button button-red" href={`/user/login${$page.url.search}`}> Login/Create Account </a>
<form action="" method="POST">
    <input class="button button-white" type="submit" value="Play as a Guest">
</form>

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
