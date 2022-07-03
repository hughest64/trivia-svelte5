<script lang="ts">
	import { page } from '$app/stores';
	import QuizIcon from '$lib/icons/QuizIcon.svelte';
	import ChatIcon from './icons/ChatIcon.svelte';
	import LeaderboardIcon from './icons/LeaderboardIcon.svelte';
	import MegaroundIcon from './icons/MegaroundIcon.svelte';
	import MenuIcon from './icons/MenuIcon.svelte';
	import ScoringIcon from './icons/ScoringIcon.svelte';

	const joinCode = $page.params?.joincode;
	$: routeId = <string>$page.routeId?.split('/')[0];
	$: isEventRoute =
		['game', 'host'].indexOf(routeId) > -1 &&
		$page.routeId !== 'game/join' &&
		$page.routeId !== 'host/event-setup';
</script>

<nav>
	<ul class:justify-nav={!isEventRoute}>
		{#if isEventRoute}
			<li>
				<a href={`/${routeId}/${joinCode}`}>
					<div>
						<QuizIcon />
						<p>Quiz</p>
					</div>
				</a>
			</li>
			<li>
				<a href={`/${routeId}/${joinCode}/leaderboard`}>
					<div>
						<LeaderboardIcon />
						<p>Leaderboard</p>
					</div>
				</a>
			</li>
			<li>
				<a href={`/${routeId}/${joinCode}/chat`}>
					<div>
						<ChatIcon />
						<p>Chat</p>
					</div>
				</a>
			</li>
		{/if}
		{#if routeId === 'game' && isEventRoute}
			<li>
				<a href={`/game/${joinCode}/megaround`}>
					<div>
						<MegaroundIcon />
						<p>Megaround</p>
					</div>
				</a>
			</li>
		{:else if routeId === 'host' && isEventRoute}
			<li>
				<a href={`/host/${joinCode}/score`}>
					<div>
						<ScoringIcon />
						<p>Scoring</p>
					</div>
				</a>
			</li>
		{/if}
		<!-- TODO: this should open the menu component not log out directly -->
		<li>
			<a rel="external" href="/user/logout">
				<div>
					<MenuIcon />
					<p>Logout</p>
				</div>
			</a>
		</li>
	</ul>
</nav>

<style lang="scss">
	nav {
		font-size: 1.2em;
	}
	ul {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin: 0 auto;
		max-width: calc(100% - 2em);
	}
	li {
		padding: 0;
		margin: 0;
	}
	li > a {
		// padding: 0.5em;
		text-decoration: none;
	}
	div {
		width: 4em;
		height: 4em;
		background-color: #fcfcfc;
		border-radius: 0.5em;
		margin: auto;
		padding: 0.25em;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	a:hover,
	a:focus {
		text-decoration: none;
	}
	// svg {
	// 	height: 2.5em;
	// 	width: 2.5em;
	// 	&:not(.no-color-change) path {
	// 		fill: #413f43;
	// 		stroke: #413f43;
	// 	}
	// }
	p {
		font-size: 10px;
		margin: 5px 0;
		color: var(--color-black);
	}
	.justify-nav {
		justify-content: flex-end;
		// margin: 0.5em;
	}
</style>
