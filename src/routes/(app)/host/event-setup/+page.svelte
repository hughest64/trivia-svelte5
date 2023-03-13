<script lang="ts">
    import { page } from '$app/stores';
    import type { GameSelectData, LocationSelectData } from '$lib/types';

    $: form = $page.form;
    $: gameSelectData = <GameSelectData[]>$page.data?.game_select_data || [];
    $: locationSelectData = <LocationSelectData[]>$page.data?.location_select_data || [];

    // TODO: set to the host's "home" location
    let selectLocation: string;
    let selectedGame: string;
</script>

<svelte:head><title>Trivia Mafia | Event Setup</title></svelte:head>

<main class="short">
    <h1>Choose a Trivia Event</h1>

    <form action="?/fetchEventData" method="POST">
        {#if form?.error}<p class="error">{form?.error}</p>{/if}
        <label class="select-label" for="game-select">Choose your Game</label>
        <select class="select" name="game-select" id="game-select" bind:value={selectedGame}>
            {#each gameSelectData as game (game.game_id)}
                <option value={game.game_id}>{game.game_title}</option>
            {/each}
        </select>

        <label for="loaction-select" class="select-label">Choose your Venue</label>
        <select class="select" name="location-select" id="location-select" bind:value={selectLocation}>
            {#each locationSelectData as location (location.location_id)}
                <option value={location.location_id}>{location.location_name}</option>
            {/each}
        </select>

        <button class="button button-primary" type="submit" name="submit" id="submit">Begin Event</button>
    </form>
</main>
