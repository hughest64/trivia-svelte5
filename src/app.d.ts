/// <reference types="@sveltejs/kit" />

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare namespace App {
    interface Locals {
        fetchHeaders?: Record<string, string>,
        jwt?: string
        initialRoundNumber?: string | number
        initialQuestionNumber?: string | number
    }
    // interface PageData {
    //     initialRoundNumber?: string | number
    //     initialQuestionNumber?: string | number
    // }
    // interface Platform {}
}

declare namespace svelte.JSX {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    interface HTMLAttributes<T> {
        onswipe?: (event: CustomEvent) => Promise<void>;
    }
}
