<script lang="ts">
    import { fade, fly, scale } from 'svelte/transition';
    import { page } from '$app/stores';
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';
    import type { EventData } from '$lib/types';

    $: form = $page.form;
    $: console.log(form);
    $: eventData = form?.event_data satisfies EventData | null;

    const userData = getStore('userData');
    $: activeTeam = $userData?.teams.find((team) => team.id === $userData?.active_team_id);
</script>

<svelte:head><title>Trivia Mafia | Join</title></svelte:head>

<main class="short">
    {#if !!userData}
        <h1 class="team-header">Team</h1>
        <h2>{activeTeam?.name}</h2>
        <div class="line" />
    {/if}

    {#if !eventData}
        <div class="max-width text-center" in:scale={{ delay: 500, duration: 1000 }} out:fade={{ duration: 100 }}>
            <h1>Enter Game Code</h1>
            <form action="?/checkevent" method="POST" use:enhance>
                {#if form?.error}<p class="error">{form?.error}</p>{/if}
                {#if form?.reason === 'player_limit_exceeded'}
                    <a href="/team/create">Go here to create a new team</a>
                {/if}
                <div class="input-container">
                    <input
                        type="text"
                        name="joincode"
                        id="joincode"
                        autocapitalize="none"
                        autocomplete="off"
                        required
                    />
                    <label for="joincode">Game Code</label>
                </div>
                <button class="button button-primary" type="submit">Join Game!</button>
            </form>
        </div>
    {:else}
        <div
            class="max-width text-center"
            in:fly={{ y: 500, delay: 200, duration: 1000 }}
            out:fly={{ y: 500, delay: 200, duration: 500 }}
        >
            <h1>Game Code</h1>
            <form action="?/joinevent" method="post">
                {#if form?.error}<p class="error">{form?.error}</p>{/if}
                <input
                    type="text"
                    class="joincode-detail"
                    name="joincode"
                    id="joincode"
                    value={eventData?.joincode || 1234}
                    readonly
                />

                <h2 class="event-detail">You're Playing at:</h2>
                <h3 class="event-detail">{eventData?.location || 'A Fake Place'}</h3>

                <button class="button button-primary" type="submit">Looks Good</button>
            </form>
            <button class="button button-secondary" on:click={() => (eventData = null)}> That's Not Right </button>
        </div>
    {/if}
</main>

<style lang="scss">
    .team-header {
        margin-bottom: 0;
    }
    .line {
        height: 2px;
        width: min(30rem, calc(100% - 1rem));
        margin: 1rem 0 2rem;
        background-color: var(--color-primary);
    }
    .joincode-detail {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        border: none;
        outline: none;
    }
    .event-detail {
        text-align: center;
    }
</style>
