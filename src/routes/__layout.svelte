<script context="module">
    // use load function to make a fetch call to Django
    // return user details, if not logged in redirect
    // to /login, otherwise set user info in session store
    // probably and eventually team data
    // @ts-ignore - TODO how to type the SvelteKit fetch api in typescript?
    // export async function load({ fetch }) {
    //     // we could load the session and only make this call if the username is
    //     // not populated (i.e. page load or if we explicilty unset if for some reason)
    //     const response = await fetch(
    //         'http://localhost:8000/user/test'
    //     )
    //     console.log(response)
    //     if (response.ok) {
    //         const data = await response.json()
    //         return {
    //             props: {
    //                 data
    //             }
    //         }
    //     }
    // }
</script>
<script lang="ts">
    import '$lib/styles.css'
    import Footer from '$lib/Footer.svelte'

    export let data: unknown;
    $: console.log(data)
</script>

<main>
    <slot />
</main>

<footer>
    <Footer />
</footer>