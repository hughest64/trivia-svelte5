<script lang="ts">
	import { page } from '$app/stores';

	const joinCode = $page.params?.joincode;
	$: routeId = <string>$page.routeId?.split('/')[0];
	$: isEventRoute = ['game', 'host'].indexOf(routeId) > -1 && $page.routeId !== 'game/join';
</script>

<nav>
	<ul>
		{#if isEventRoute}
			<li><a href={`/${routeId}/${joinCode}`}>Game</a></li>
			<li><a href={`/${routeId}/${joinCode}/leaderboard`}>Leaderboard</a></li>
			<li><a href={`/${routeId}/${joinCode}/chat`}>Chat</a></li>
		{/if}
		{#if routeId === 'game' && isEventRoute}
			<li><a href={`/game/${joinCode}/megaround`}>Megaround</a></li>
		{/if}
        <!-- TODO: this should open the menu component not log out directly -->
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
		padding: 0.5em;
		text-decoration: none;
	}
	a:hover,
	a:focus {
		text-decoration: underline;
	}
</style>
