<script context="module" lang="ts">
    import { browser } from '$app/env';
    import { userdata, userteams } from '../stores/user';
    // import type { UserData, UserTeam } from '../stores/user';
    import type { Load } from '@sveltejs/kit';

    export const load: Load = async ({ fetch }) => {
        if (!browser) return { status: 200 }

        const response = await fetch(
            // TODO: store the host portion of the url in env
            // if dev use localhost, if prod use ...
            'http://localhost:8000/userteams/',
            {
                headers: {
                    accept: 'application/json'
                },
                credentials: 'include'
            }
        )

        if (response.ok) {
            const { user_teams, user_data} = (await response.json()) || {}
            userdata.set({ ...user_data })
            userteams.set([...user_teams])

            return { status: 200 }
        } else {
            // not logged in.
            return {
                redirect: '/user/login',
                status: 302
            }
        }
    }
</script>

<script lang="ts">
    import '$lib/styles.css'
    import Footer from '$lib/Footer.svelte'
</script>

<main>
    <slot />
</main>

<footer>
    <Footer />
</footer>