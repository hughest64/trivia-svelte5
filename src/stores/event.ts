import { writable } from "svelte/store";
/**
 * Store contianing event related data
 */

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


