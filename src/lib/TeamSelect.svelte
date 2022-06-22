<script lang="ts">
	import { goto } from '$app/navigation';
	import { userdata, userteams, useractiveteam, type UserTeam } from '$stores/user';
	const apiHost = import.meta.env.VITE_API_HOST

	// TODO: add create a team and join by code (team password)
	// TODO: handle when there are no teams (probably just hide the select)
	let selected: UserTeam = $useractiveteam || $userteams[0]; 

	const handleTeamSelectSubmit = async () => {
		console.log('you have chosen to play with', selected.team_name);

		if (selected.team_id === $userdata.active_team_id) {
			goto('/game/join')

		} else {
			// TODO: this should send the csrf token (hopefully it's in the session store!)
			// for csrf validation
			const response = await fetch(
				`${apiHost}/teamselect/`,
				{
					method: 'POST',
					credentials: 'include',
					headers: {'content-type': 'application/json' },
					body: JSON.stringify({ team_id: selected.team_id })
				}
			);
			if (response.ok) {
				const active_team_id = await response.json()
				userdata.update(data => ({ ...data, ...active_team_id }))
				goto('/game/join')
			}
		}
        // TODO: handle not ok
	};
</script>

<h1>Team Select</h1>

<form class="container" on:submit|preventDefault={handleTeamSelectSubmit}>
	<h2>{$userdata?.username} Select A Team</h2>
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
