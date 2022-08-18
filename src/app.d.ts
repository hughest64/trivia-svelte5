/// <reference types="@sveltejs/kit" />

// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare namespace App {
    interface Locals {
        userdata: import('$stores/user').UserData;
    }
    // interface Platform {}
}

declare namespace svelte.JSX {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    interface HTMLAttributes<T> {
        onswipe?: (event: CustomEvent) => Promise<void>;
    }
}
