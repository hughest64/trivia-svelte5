import { writable, derived } from "svelte/store";
import type { Readable, Writable } from 'svelte/store'
/**
 * Store contianing event related data
 */

export interface EventQuestion {
    id: string | number;
    text: string;
    answer: string;
    question_number: number;
    question_type: string;
    question_url: string;
    question_displayed: boolean;
    answer_displayed: boolean;
}

export interface EventRound {
    id: string | number;
    title: string;
    description: string;
    round_number: number;
    locked: boolean;
    scored: boolean;
    questions: EventQuestion[];
}

export interface EventData {
    event_id: string | number;
    game_id: string | number;
    game_title: string;
    location: string;
    join_code: string | number;
    reveal_answers: boolean;
    current_round_number: number;
    current_question_number: number;
    rounds: EventRound[];
}

// this store is used as a temporary container of data from /game/join
// it then gets split up to the other stores in the game __layout
export const eventData: Writable<EventData> = writable();

export const roundNumbers: Writable<number[]> = writable()

export const eventRounds: Writable<EventRound[]> = writable()
export const currentRoundNumber: Writable<number> = writable()
export const currentQuestionNumber: Writable<number> = writable()

export const currentRound: Readable<EventRound> = derived(
    [eventRounds, currentRoundNumber],
    ([$eventRounds, $currentRoundNumber]) => {
        const index =  $eventRounds?.findIndex(
            round => round.round_number === $currentRoundNumber
        ) || 0
        return $eventRounds[index]
    }
)

export const currentQuestion: Readable<EventQuestion> = derived(
    [currentRound, currentQuestionNumber],
    ([$currentRound, $currentQuestionNumber]) => {
        const index =  $currentRound?.questions.findIndex(
            q => q.question_number === $currentQuestionNumber
        ) || 0
        return $currentRound?.questions[index]
    }
)


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


