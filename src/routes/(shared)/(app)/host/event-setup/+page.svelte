<script lang="ts">
    import '$lib/styles/host.scss';
    import { page } from '$app/stores';
    import { EventSetupManager } from './event-manager.svelte';

    let { form, data } = $props();
    // $inspect('data', data);

    let evm = new EventSetupManager(data);
    // $inspect(evm.visbleBlocks);
    let buttontext = $derived(evm.selectedEventExists ? 'Join Trivia Event' : 'Begin Trivia Event');
</script>

<svelte:head><title>Trivia Mafia | Event Setup</title></svelte:head>

<main class="short">
    <h1>Choose a Trivia Event</h1>

    <form action="?/fetchEventData" method="POST">
        {#if form?.error}<p class="error">{form?.error}</p>{/if}

        <div class="switch-container">
            <h4>Use Sound Round?</h4>
            <label for="sound-choice" class="switch">
                <input type="checkbox" bind:checked={evm.useSound} name="sound-choice" />
                <button
                    id="sound-btn"
                    class="slider round"
                    class:revealed={evm.useSound}
                    on:click|preventDefault={() => evm.toggleUseSound()}
                />
            </label>
        </div>

        <div class="switch-container">
            <h4>Theme Night?</h4>
            <label for="event_type" class="switch">
                <input type="checkbox" bind:checked={evm.useThemeNight} name="event_type" />
                <button
                    id="event-type-btn"
                    class="slider round"
                    class:revealed={evm.useThemeNight}
                    on:click|preventDefault={() => evm.toggleUseThemeNight()}
                />
            </label>
        </div>

        <div class="switch-container">
            <h4>Limit Teams to Single Device?</h4>
            <label for="player_limit" class="switch">
                <input type="checkbox" bind:checked={evm.playerLimit} name="player_limit" />
                <button
                    id="player-limit-btn"
                    class="slider round"
                    class:revealed={evm.playerLimit}
                    on:click|preventDefault={() => evm.togglePlayerLimit()}
                />
            </label>
        </div>

        <label class="select-label" for="block-select">Choose A Block</label>
        <select class="select" name="block-select" id="block-select" bind:value={evm.selectedBlock}>
            {#each evm.visibleBlocks as block}
                <option value={block}>{block}</option>
            {/each}
        </select>

        <label for="location_select" class="select-label">Choose your Venue</label>
        <select class="select" name="location_select" id="location_select" bind:value={evm.selectedLocation}>
            {#each evm.location_select_data as location (location.location_id)}
                <option value={location.location_id}>{location.location_name}</option>
            {/each}
        </select>

        <h2>You've Selected</h2>
        <p id="selected-game">{evm.selectedGame?.game_title || 'No Matching Game'}</p>
        <input
            class="selected-game"
            type="hidden"
            name="game_select"
            id="game_select"
            value={evm.selectedGame?.game_id}
        />

        <button
            class="button button-primary"
            type="submit"
            name="submit"
            id="submit"
            disabled={!evm.selectedGame?.game_id}
        >
            {buttontext}
        </button>
    </form>
    <small>Click <a href="/host/event-setup/recent" data-sveltekit-reload>here</a> to view your recent games</small>
</main>

<style lang="scss">
    .switch-container {
        display: flex;
        justify-content: space-between;
        width: min(var(--max-element-width), 100%);
        margin-left: 0;
        label {
            margin-right: 0;
        }
    }
    button:disabled {
        color: gray;
    }
</style>
