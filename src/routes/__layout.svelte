<script context="module" lang="ts">
    import { browser } from '$app/env';
    import type { Load } from '@sveltejs/kit';

    export const load: Load = async ({ fetch, session }) => {
        if (browser) {
            return {
                status: 200
            }
        }
        const response = await fetch(
            // TODO: store the host portion of the url in env
            // if dev use localhost, if prod use ...
            'http://localhost:8000/user/',
            { credentials: 'include' }
        )

        if (response.ok) {
            const data = await response.json()
            session.data = data

            return {
                // status: 200,
                stuff: data,
            }
        } else {
            // not logged in.
            return {
                redirect: '/user/login',
                status: 302
            }
        }
        // return { status: 200 }
    }
</script>
<script lang="ts">
    import '$lib/styles.css'
    import Footer from '$lib/Footer.svelte'
    import { session } from '$app/stores';

    $: console.log('session from layout', $session)
    
</script>

<main>
    <slot />
</main>

<footer>
    <Footer />
</footer>