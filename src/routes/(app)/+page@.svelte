<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { fly, scale } from 'svelte/transition';

    $: form = $page.form;
    $: loaderror = $page.data.loaderror;
    let showContent = false;
    onMount(() => (showContent = true));
</script>

<svelte:head><title>Trivia Mafia | Welcome</title></svelte:head>

<main>
    {#if showContent}
        <div transition:scale|local={{ duration: 1500 }} class="logo-container">
            <img src="TMLogo-2023_TM-Stacked-RedBlack.svg" alt="Trivia Mafia" />
        </div>

        <div transition:fly|local={{ y: 500, duration: 1500 }} class="form-container flex-column">
            {#if loaderror}
                <h3>{loaderror}</h3>
            {:else}
                <a class="button button-primary" href={`/user/login${$page.url.search}`}> Login/Create Account </a>
                <form action="/user/create{$page.url.search}" method="POST">
                    <input type="hidden" name="guest_user" value="true" />
                    <button class="button button-tertiary" type="submit">Play As a Guest</button>
                </form>
                {#if form?.error}<p>{form?.error}</p>{/if}
            {/if}
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
</style>
