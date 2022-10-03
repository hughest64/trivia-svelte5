/// <reference types="@sveltejs/kit" />

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare namespace App {
    interface Locals {
        fetchHeaders?: Record<string, string>,
        // jwt?: string
        activeRoundNumber?: string | number
        activeQuestionNumber?: string | number
    }
    // interface PageData {}
    // interface Platform {}
}

declare namespace svelte.JSX {
    interface HTMLAttributes {
        onswipe?: (event: CustomEvent) => Promise<void>;
    }
}
