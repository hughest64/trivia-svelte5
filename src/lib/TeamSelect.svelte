<script lang="ts">
	import { goto } from '$app/navigation';
	import { userdata, userteams, type UserTeam } from '$stores/user';

	let selected: UserTeam;

	const handleTeamSelectSubmit = async () => {
		// post to the api and if resp.ok, goto gameselct (or next=/some/place)
		console.log('you have chosen to play with', selected.team_name);
		// update current team if different that what is in the store (post to the api)
		// goto /game/game-selct (join?)
		const response = await fetch(
			'http://localhost:8000/teamselect/',
			{
				method: 'POST',
				credentials: 'include',
				headers: {'content-type': 'application/json' },
				// TODO: we might acutally just send a team id
				// to have the server set active team id for the user
				body: JSON.stringify(selected)
			}
		);
		if (response.ok) {
            // TODO: update active team in the store?
            goto('/game/game-select')
        }
        // TODO: handle not ok
	};
</script>

<h1>Team Select</h1>

<form class="container" on:submit|preventDefault={handleTeamSelectSubmit}>
	<h2>{$userdata.username} Select A Team</h2>
	<select bind:value={selected}>
		{#each $userteams as team (team.team_id)}
			<option value={team}>{team.team_name}</option>
		{/each}
	</select>
	<input type="submit" value="Choose This Team" />
</form>

<style>
	.container {
		display: flex;
		flex-direction: column;
		justify-content: center;
		gap: 0.75em;
		max-width: 30rem;
		margin: 5rem auto 0;
	}
</style>
