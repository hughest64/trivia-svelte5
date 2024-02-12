<script lang="ts">
    import '$lib/styles/host.scss';
    import { page } from '$app/stores';

    $: form = $page.form;
    const gameSelectData = $page.data?.game_select_data || [];
    const locationSelectData = $page.data?.location_select_data || [];
    const gameBlocks = ($page.data?.game_block_data || []).sort();
    const nonThemeBlocks = gameBlocks.filter((b) => ['a', 'b', 'c', 'd'].includes(b.toLocaleLowerCase()));
    const themeBlocks = gameBlocks.filter((b) => !['a', 'b', 'c', 'd'].includes(b.toLocaleLowerCase()));

    const todaysEvents = $page.data?.todays_events || [];

    let useSound = !!locationSelectData[0]?.use_sound;
    let selectedLocation = locationSelectData[0]?.location_id;
    let playerLimit = false;
    let useThemeNight = false;

    let selectedBlock = useThemeNight ? themeBlocks[0] : nonThemeBlocks[0];

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

    const handleUseThemeNight = () => {
        useThemeNight = !useThemeNight;
        selectedBlock = useThemeNight ? themeBlocks[0] : nonThemeBlocks[0];
    };
</script>

<svelte:head><title>Trivia Mafia | Event Setup</title></svelte:head>

<main class="short">
    <h1>Choose a Trivia Event</h1>

    <form action="?/fetchEventData" method="POST">
        {#if form?.error}<p class="error">{form?.error}</p>{/if}

        <div class="switch-container">
            <h4>Use Sound Round?</h4>
            <label for="sound-choice" class="switch">
                <input type="checkbox" bind:checked={useSound} name="sound-choice" />
                <button
                    id="sound-btn"
                    class="slider round"
                    class:revealed={useSound}
                    on:click|preventDefault={() => (useSound = !useSound)}
                />
            </label>
        </div>

        <div class="switch-container">
            <h4>Theme Night?</h4>
            <label for="event_type" class="switch">
                <input type="checkbox" bind:checked={useThemeNight} name="event_type" />
                <button
                    id="event-type-btn"
                    class="slider round"
                    class:revealed={useThemeNight}
                    on:click|preventDefault={handleUseThemeNight}
                />
            </label>
        </div>

        <div class="switch-container">
            <h4>Limit Game to Single Device?</h4>
            <label for="player_limit" class="switch">
                <input type="checkbox" bind:checked={playerLimit} name="player_limit" />
                <button
                    id="player-limit-btn"
                    class="slider round"
                    class:revealed={playerLimit}
                    on:click|preventDefault={() => (playerLimit = !playerLimit)}
                />
            </label>
        </div>

        <label class="select-label" for="block-select">Choose A Block</label>
        <select class="select" name="block-select" id="block-select" bind:value={selectedBlock}>
            {#each useThemeNight ? themeBlocks : nonThemeBlocks as block}
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

        <h2>You've Selected</h2>
        <p>{selectedGame?.game_title || ''}</p>
        <input class="selected-game" type="hidden" name="game_select" id="game_select" value={selectedGame?.game_id} />

        <button class="button button-primary" type="submit" name="submit" id="submit">{buttontext}</button>
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
</style>
