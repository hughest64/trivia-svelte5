/// <reference types="@sveltejs/kit" />

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare namespace App {
    interface Locals {
        fetchHeaders?: Record<string, string>
        loaded?: boolean
        // jwt?: string
        activeRoundNumber?: string | number
        activeQuestionNumber?: string | number
    }
    interface PageData {
        user_data?: import('$lib/types').UserData;
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
