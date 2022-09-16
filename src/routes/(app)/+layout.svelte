<script lang="ts">
    import { page } from '$app/stores';
    import Footer from '$lib/footer/Footer.svelte';
    import Menu from '$lib/Menu.svelte';
    import { fly } from 'svelte/transition';
    import {
        activeRoundNumber,
        activeQuestionNumber,
        currentRoundNumber,
        currentQuestionNumber,
        setEventStores
    } from '$stores/event';

    import Stores from '$lib/Stores.svelte';
    
    const data = $page.data;
    
    $: data.event_data && setEventStores($page.data.event_data);

    $: activeRoundNumber.set(Number(data.initialRoundNumber) || $currentRoundNumber || 1);
    $: activeQuestionNumber.set(Number(data.initialQuestionNumber) || $currentQuestionNumber || 1);

    let displayMenu = false;
</script>

{#if displayMenu}
    <div transition:fly={{ y: -2000, duration: 800 }}>
        <Menu on:click={() => (displayMenu = false)} />
    </div>
{/if}

<Stores>
    <slot />
</Stores>

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
