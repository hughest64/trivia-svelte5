<script lang="ts">
    import { page } from '$app/stores'

    const joinCode = $page.params?.joincode
    const routeId = <string>$page.routeId?.split('/')[0]
</script>

<nav>
    <ul>
        <li><a href="/" >Home</a></li>
        {#if ['game', 'host'].indexOf(routeId) > -1}
            <li><a href={`/${routeId}/${joinCode}/leaderboard`}>Leaderboard</a></li>
            <li><a href={`/${routeId}/${joinCode}/chat`}>Chat</a></li> 
        {/if}
        {#if routeId === 'game'}
            <li><a href={`/game/${joinCode}/megaround`}>Megaround</a></li>
        {/if}
        <li><a href="/user">Settings</a></li>
        <li><a href="/user/login">Login</a></li>
        <li><a href="/user/logout">Logout</a></li>
    </ul>
</nav>

<style>
    nav {
        border-top: 2px solid #000;
        font-size: 1.25em;
    }
    ul {
        display: flex;
        justify-content: space-evenly;
        margin: 0;
        padding: 1em;
        list-style: None;
    }
    li {
        padding: 0;
        margin: 0;
    }
    li > a {
        padding: .5em;
        text-decoration: none;
    }
    a:hover, a:focus {
        text-decoration: underline;
    }
</style>