<script context="module">
    import { browser } from '$app/env';

    // @ts-ignore - TODO how to type the SvelteKit fetch api in typescript?
    export async function load({ fetch, session }) {
        // TODO: will this validate proplery in Django if we login from here first? (i.e. origin is :3000)
        // run the user request server side
        if (browser) {
            return {
                status: 200
            }
        }
        // TODO: this may need to be a post, or add a custom X-Username header
        // see https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
        const response = await fetch(
            // TODO: store the host portion of the url in env
            // if dev use localhost, if prod use ...
            'http://localhost:8000/user/'
        )

        // if (response.ok) {
        //         const data = await response.json()
        //         session.data = data

        //     return {
        //         status: 200
        //     }
        // } else {
        //     // not logged in.
        //     return {
        //         redirect: '/user/login',
        //         status: 302
        //     }
        // }
        return { status: 200 }
    }
</script>
<script lang="ts">
    import '$lib/styles.css'
    import Footer from '$lib/Footer.svelte'
    import { session } from '$app/stores';

    $: console.log('session', $session)
    
</script>

<main>
    <slot />
</main>

<footer>
    <Footer />
</footer>