/**
 * Store containing event related data
 */
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';
import type { EventRound, /** EventQuestion */ } from '$lib/types';

// boolean that is set when the event stores are populated
export const eventDataLoaded: Writable<boolean> = writable(false);

export const roundNumbers: Writable<number[]> = writable();
export const eventRounds: Writable<EventRound[]> = writable();

// comes from the database and represents current game progress
export const currentRoundNumber: Writable<number> = writable();
export const currentQuestionNumber: Writable<number> = writable();

// usually comes from a cookie and represents what a user is viewing
export const activeRoundNumber: Writable<number> = writable();
export const activeQuestionNumber: Writable<number> = writable();

/** Web socket payload from get_event_data in the current version
{
    // event store
    "event": event, // round locks, revealed questions, displayed answers, etc
    "game": game, // questions, rounds, etc
    "max_scored_round": event_obj.max_scored_round,
    "is_host": is_host, // maybe not relevant?
    
    // chat store (could be team as well)
    "host_chats": [chat.serialize() for chat in host_chats], // leave for fetching at /chat
    
    // response store
    "responses": responses, // move to a separate store

    // leaderboard store
    "leaderboard": event_obj.get_leaderboard(),
    "leaderboard_entry_id": (
        leaderboard_entry.id if leaderboard_entry else None
        ),
    "selected_megaround": team_megaround, // just part of the leaderboard ?
}
*/
