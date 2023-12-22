<script lang="ts">
    import { page } from '$app/stores';
    import type { EventData } from '$lib/types';

    type RecentEvent = Omit<EventData, 'current_round_number' | 'current_question_number'>;
    const recentEvents: RecentEvent[] = $page.data.recent_events;
</script>

<svelte:head><title>Trivia Mafia | Recent Games</title></svelte:head>

<main>
    <h1>Recent Hosted Events</h1>
    <ul>
        {#each recentEvents as event (event.event_id)}
            <li class="event-entry flex-column">
                <h4>{event.game_title} @ {event.location}</h4>
                <h4>Joincode: <a href="/host/{event.joincode}" data-sveltekit-reload>{event.joincode}</a></h4>
            </li>
        {/each}
    </ul>
</main>

<style lang="scss">
    .event-entry {
        border: 2px solid var(--color-secondary);
        border-radius: 10px;
        margin-bottom: 1rem;
        padding: 0 1rem;

        h4 {
            margin: 0.5rem;
        }
    }
</style>
