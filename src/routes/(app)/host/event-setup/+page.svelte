<script lang="ts">
    import '$lib/styles/host.scss';
    import { page } from '$app/stores';

    $: form = $page.form;
    const gameSelectData = $page.data?.game_select_data || [];
    const locationSelectData = $page.data?.location_select_data || [];
    const gameBlocks = ($page.data?.game_block_data || []).sort();
    const todaysEvents = $page.data?.todays_events || [];

    let selectedBlock = gameBlocks[0];

    let useSound = locationSelectData[0].use_sound;
    let selectedLocation = locationSelectData[0].location_id;
    let playerLimit = false;

    $: selectedGame = gameSelectData.filter((g) => g.block === selectedBlock && g.use_sound === useSound)[0];
    $: selectedEventExists = !!todaysEvents.find(
        (e) => e.location_id === selectedLocation && e.game_id === selectedGame?.game_id
    );
    $: buttontext = selectedEventExists ? 'Join Trivia Event' : 'Begin Trivia Event';

    const handleLocationChange = (event: Event) => {
        const target = event.target as HTMLSelectElement;
        const newloc = locationSelectData.find((l) => String(l.location_id) === target.value);
        useSound = newloc?.use_sound === false ? false : true;
    };
</script>

<svelte:head><title>Trivia Mafia | Event Setup</title></svelte:head>

<main class="short">
    <h1>Choose a Trivia Event</h1>

    <form action="?/fetchEventData" method="POST">
        {#if form?.error}<p class="error">{form?.error}</p>{/if}

        <div class="switch-container">
            <h4>Use Sound Round</h4>
            <label for="sound-choice" class="switch">
                <input type="hidden" bind:value={useSound} name="sound-choice" />
                <button
                    id="sound-btn"
                    class="slider"
                    class:revealed={useSound}
                    on:click|preventDefault={() => (useSound = !useSound)}
                />
            </label>
        </div>

        <div class="switch-container">
            <h4>Limit Game to Single Device</h4>
            <label for="player_limit" class="switch">
                <input type="hidden" bind:value={playerLimit} name="player_limit" />
                <button
                    id="player-limit-btn"
                    class="slider"
                    class:revealed={playerLimit}
                    on:click|preventDefault={() => (playerLimit = !playerLimit)}
                />
            </label>
        </div>

        <label class="select-label" for="block-select">Choose A Block</label>
        <select class="select" name="block-select" id="block-select" bind:value={selectedBlock}>
            {#each gameBlocks as block}
                <option value={block}>{block}</option>
            {/each}
        </select>

        <label for="location_select" class="select-label">Choose your Venue</label>
        <select
            class="select"
            name="location_select"
            id="location_select"
            bind:value={selectedLocation}
            on:change={handleLocationChange}
        >
            {#each locationSelectData as location (location.location_id)}
                <option value={location.location_id}>{location.location_name}</option>
            {/each}
        </select>

        <label class="" for="game_select"><h2>You've Selected</h2></label>
        <input
            class="selected-game"
            type="text"
            name="game_select"
            id="game_select"
            readonly
            value={selectedGame?.game_title}
        />

        <button class="button button-primary" type="submit" name="submit" id="submit">{buttontext}</button>
    </form>
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
    .selected-game {
        border: None;
        font-size: 24px;
    }
</style>
