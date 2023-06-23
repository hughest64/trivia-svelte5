/// <reference types="@sveltejs/kit" />

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare namespace App {
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
        user_data?: import('$lib/types').UserData;
        event_data?: import('$lib/types').EventData;
        current_event_data?: import('$lib/types').CurrentEventData;
        rounds?: Array<import('$lib/types').GameRound>;
        questions?: Array<import('$lib/types').GameQuestion>;
        round_states?: Array<import('$lib/types').EventRound>;
        question_states?: Array<import('$lib/types').EventQuestion>;
        location_select_data?: Array<import('$lib/types').LocationSelectData>;
        game_select_data?: Array<import('$lib/types').GameSelectData>;
        game_block_data?: string[];
        player_joined?: boolean;
    }
    // interface Platform {}
    interface Error {
        next?: string;
        code?: string | number;
    }
}

declare namespace svelteHTML {
    interface HTMLAttributes<T> {
        'on:swipe'?: (event: CustomEvent) => Promise<void>;
    }
}
