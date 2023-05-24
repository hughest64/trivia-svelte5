<script lang="ts">
    import '$lib/styles/host.scss';
    import { page } from '$app/stores';

    $: form = $page.form;
    const gameSelectData = $page.data?.game_select_data || [];
    const locationSelectData = $page.data?.location_select_data || [];
    const gameBlocks = ($page.data?.game_block_data || []).sort();

    // TODO: default based on a user setting?
    let useSound = true;

    // TODO: default based on a user setting?
    let selectedBlock = gameBlocks[0];
    $: availableGames = gameSelectData.filter((g) => g.block === selectedBlock && g.use_sound === useSound);

    // TODO: set to the host's "home" location
    let selectLocation: string;
    $: selectedGame = availableGames[0].game_id;
</script>

<svelte:head><title>Trivia Mafia | Event Setup</title></svelte:head>

<main class="short">
    <h1>Choose a Trivia Event</h1>

    <div class="switch-container">
        <h4>Use Sound</h4>
        <label for="sound-choice" class="switch">
            <input type="hidden" bind:value={useSound} name="sound-choice" />
            <button class="slider" class:revealed={useSound} on:click={() => (useSound = !useSound)} />
        </label>
    </div>

    <label class="select-label" for="block-select">Choose A Block</label>
    <select class="select" name="block-select" id="block-select" bind:value={selectedBlock}>
        {#each gameBlocks as block}
            <option value={block}>{block}</option>
        {/each}
    </select>

    <form action="?/fetchEventData" method="POST">
        {#if form?.error}<p class="error">{form?.error}</p>{/if}
        <label class="select-label" for="game-select">Choose your Game</label>
        <select class="select" name="game-select" id="game-select" bind:value={selectedGame}>
            {#each availableGames as game (game.game_id)}
                <option value={game.game_id}>{game.game_title}</option>
            {/each}
        </select>

        <label for="loaction-select" class="select-label">Choose your Venue</label>
        <select class="select" name="location-select" id="location-select" bind:value={selectLocation}>
            {#each locationSelectData as location (location.location_id)}
                <option value={location.location_id}>{location.location_name}</option>
            {/each}
        </select>

        <button class="button button-primary" type="submit" name="submit" id="submit">Host Event</button>
    </form>
</main>

<style lang="scss">
    .switch-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        width: 100%;
        max-width: var(--max-element-width);
        label {
            margin-left: 0;
        }
    }
</style>
