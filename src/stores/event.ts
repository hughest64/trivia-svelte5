/**
 * Store containing event related data
 */
import { writable, derived } from 'svelte/store';
import type { Readable, Writable } from 'svelte/store';
import type { EventData, EventRound, EventQuestion } from '$lib/types';

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

export const activeRound: Readable<EventRound> = derived(
    [eventRounds, activeRoundNumber],
    ([$eventRounds, $activeRoundNumber]) => {
        const index = $eventRounds?.findIndex((round) => round.round_number === $activeRoundNumber);
        return $eventRounds[index];
    }
);

export const activeQuestion: Readable<EventQuestion> = derived(
    [activeRound, activeQuestionNumber],
    ([$activeRound, $activeQuestionNumber]) => {
        const index = $activeRound?.questions.findIndex((q) => q.question_number === $activeQuestionNumber) || 0;
        return $activeRound?.questions[index];
    }
);

export const setEventStores = (data: EventData) => {
    roundNumbers.set(data.rounds.map((round) => round.round_number));
    currentRoundNumber.set(data.current_round_number);
    currentQuestionNumber.set(data.current_question_number);
    eventRounds.set(data.rounds);
    eventDataLoaded.set(true);
};

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
