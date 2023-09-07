import * as types from '$lib/types';

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
    namespace App {
        interface Locals {
            fetchHeaders?: Record<string, string>;
            jwt?: string;
            validtoken?: boolean;
            staffuser?: boolean;
            activeRoundNumber?: string | number;
            activeQuestionNumber?: string | number;
            activeQuestionKey?: string;
            websocketHost?: string;
            updateDelay?: number;
        }
        interface PageData {
            loaderror?: string;
            user_data?: types.UserData;
            chat_messages?: Array<types.ChatMessage>;
            event_data?: types.EventData;
            current_event_data?: types.CurrentEventData;
            rounds?: Array<types.GameRound>;
            questions?: Array<types.GameQuestion>;
            tiebreaker_questions?: Array<types.GameQuestion>;
            tiebreaker_responses?: Array<types.TiebreakerResponse>;
            round_states?: Array<types.EventRound>;
            question_states?: Array<types.EventQuestion>;
            location_select_data?: Array<types.LocationSelectData>;
            game_select_data?: Array<types.GameSelectData>;
            game_block_data?: string[];
            player_joined?: boolean;
            points_adjustment_reasons?: Array<types.PointsAdjustmentReson>;
        }
        // interface Platform {}
        interface Error {
            next?: string;
            code?: string | number;
        }
    }

    namespace svelteHTML {
        interface HTMLAttributes<T> {
            'on:swipe'?: (event: CustomEvent) => Promise<void>;
        }
    }
}
