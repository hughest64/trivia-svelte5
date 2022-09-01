<script lang="ts">
    import '$lib/styles/app.scss';
    import { page } from '$app/stores';
    import Footer from '$lib/Footer.svelte';
    import Menu from '$lib/Menu.svelte';
    import { fly } from 'svelte/transition';
    import { userdata, type UserData } from '$stores/user';
    import {
        activeRoundNumber,
        activeQuestionNumber,
        currentRoundNumber,
        currentQuestionNumber,
        setEventStores
    } from '$stores/event';
    import type { PageData } from './$types';

    export let data: PageData;

    $: data?.user_data && userdata.set($page.data.user_data as UserData);
    $: data?.event_data && setEventStores($page.data.event_data);

    $: activeRoundNumber.set(Number(data?.initialRoundNumber) || $currentRoundNumber || 1);
    $: activeQuestionNumber.set(Number(data?.initialQuestionNumber) || $currentQuestionNumber || 1 );

    let displayMenu = false;
</script>

<!-- <main> -->
    {#if displayMenu}
        <div transition:fly={{ y: -2000, duration: 800 }}>
            <Menu on:click={() => (displayMenu = false)} />
        </div>
    {/if}

    <slot />
<!-- </main> -->

<footer>
    <Footer on:click={() => (displayMenu = !displayMenu)} />
</footer>

<style lang="scss">
    // :global(body) {
    // 	margin: 0;
    // 	height: 100vh;
    // }
    div {
        position: fixed;
        top: 0;
        height: calc(100% - 10em);
        width: 100%;
        overflow: hidden;
        margin: 0;
        border-bottom-left-radius: 3em;
        border-bottom-right-radius: 3em;
        background-color: #413f43;
    }
</style>
