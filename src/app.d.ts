/// <reference types="@sveltejs/kit" />

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare namespace App {
    interface Locals {
        fetchHeaders?: Record<string, string>
        jwt?: string
        validtoken?: boolean
        staffuser?: boolean
        activeRoundNumber?: string | number
        activeQuestionNumber?: string | number
        activeQuestionKey?: string
    }
    interface PageData {
        user_data?: import('$lib/types').UserData;
        event_data?: import('$lib/types').EventData;
        current_event_data?: import('$lib/types').CurrentEventData;
        rounds?: Array<import('$lib/types').GameRound>;
        questions?: Array<import('$lib/types').GameQuestion>;
        round_states?: Array<import('$lib/types').EventRound>;
        question_states?: Array<import('$lib/types').EventQuestion>;
        location_select_data?: Array<import('$lib/types').LocationSelectData>;
        game_select_data?: Array<import('$lib/types').GameSelectData>;
    }
    // interface Platform {}
}

declare namespace svelte.JSX {
    /* eslint-disable-next-line @typescript-eslint/no-unused-vars*/
    interface HTMLAttributes {
        onswipe?: (event: CustomEvent) => Promise<void>;
    }
}
