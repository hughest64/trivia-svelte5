<script lang="ts">
    import { page } from '$app/stores';
    import Footer from '$lib/Footer.svelte';
    import Menu from '$lib/Menu.svelte';
    import { fly } from 'svelte/transition';
    import { userdata } from '$stores/user';
    import {
        activeRoundNumber,
        activeQuestionNumber,
        currentRoundNumber,
        currentQuestionNumber,
        setEventStores
    } from '$stores/event';
    
    const data = $page.data;
    $: data.user_data && userdata.set($page.data.user_data);
    $: data.event_data && setEventStores($page.data.event_data);

    $: activeRoundNumber.set(Number(data.initialRoundNumber) || $currentRoundNumber || 1);
    $: activeQuestionNumber.set(Number(data.initialQuestionNumber) || $currentQuestionNumber || 1 );

    let displayMenu = false;
</script>

{#if displayMenu}
    <div transition:fly={{ y: -2000, duration: 800 }}>
        <Menu on:click={() => (displayMenu = false)} />
    </div>
{/if}

<slot />

<footer>
    <Footer on:click={() => (displayMenu = !displayMenu)} />
</footer>

<style lang="scss">
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
