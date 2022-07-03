<script lang="ts">
    import { page } from '$app/stores'
    import { goto } from '$app/navigation'
    import { userdata } from '$stores/user';
    import { getFetchConfig } from '$lib/utils'

    const apiHost = import.meta.env.VITE_API_HOST

    let message = ''

    const handleGuestClick = async(event: MouseEvent) => {
        const target = <HTMLAnchorElement>event.target;
        message = 'logging in'

        const response = await fetch(
            `${apiHost}/user/guest`,
            getFetchConfig("POST")
        )

        if (response.ok) {
            const data = await response.json()
            data  && userdata.set(data)
            goto(target.href)
        }
        else {
            console.log("oopsy!")
            message = "oops!"
        }
    }
</script>

<svelte:head><title>Trivia Mafia | Welcome</title></svelte:head>


<div class="logo-container">    
    <img src="TM2021-Flat-Stacked-WhiteBackground.svg" alt="Trivia Mafia">
</div>

{#if message} <p>Oops!</p> {/if}

<!-- rel=external disables internal navigation and ensures that we hit the api to get a csrf token for login -->
<a
    class="button button-red"
    href={`/user/login${$page.url.search}`}
    rel="external"
>
    Login/Create Account
</a>
<a
    class="button button-white"
    href={`/${$page.url.search}`}
    on:click|preventDefault={handleGuestClick}
>
    Play as a Guest
</a>

<style lang="scss">
    a {
        text-decoration: none;
    }
    .logo-container {
        margin-bottom: 4em;
        img {
            width:30em;
            max-width: calc(100% - 2em);
            margin: auto;
            display: block;
        }
}
</style>