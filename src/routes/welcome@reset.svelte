<script lang="ts">
    import { page } from '$app/stores'
    import { goto } from '$app/navigation'

    const handleGuestClick = async(event: MouseEvent) => {
        const target = <HTMLAnchorElement>event.target;

        // fetch the api to get the user set up
    
        goto(target.href)
    }

</script>

<svelte:head><title>Trivia Mafia | Welcome</title></svelte:head>

<div class="logo_container">    
    <img src="TM2021-Flat-Stacked-WhiteBackground.svg" alt="Trivia Mafia">
</div>
<a
    class="button button-red"
    href={`/user/login${$page.url.search}`}
    rel="external"
>
    Login/Create Account
</a>
<!-- TODO: this needs to hit the API to log in, so it's probably a button with a goto in the function? -->
<a
    class="button button-white"
    href={`/${$page.url.search}`}
    on:click|preventDefault={handleGuestClick}
>
    Play as a Guest
</a>

<style>
    a {
        text-decoration: none;
    }
</style>