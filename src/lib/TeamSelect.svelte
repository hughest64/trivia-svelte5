<script lang="ts">
	import { checkStatusCode, getFetchConfig } from '$lib/utils';
	import { goto } from '$app/navigation';
	import { userdata, userteams, useractiveteam, type UserTeam } from '$stores/user';
	const apiHost = import.meta.env.VITE_API_HOST;
	let hidecreateteam = true;
	let hideteampassword = true;
	// TODO: finish create a team and join by code (team password)
	// TODO: handle when there are no teams (probably just hide the select)
	let selected: UserTeam = $useractiveteam || $userteams[0];
	let message: string;

	const handleTeamSelectSubmit = async () => {
		if (selected.team_id === $userdata.active_team_id) {
			goto('/game/join');
		} else {
			// TODO: this should send the csrf token (hopefully it's in the session store!)
			// for csrf validation
			const fetchConfig = getFetchConfig('POST', { team_id: selected.team_id })
			const response = await fetch(`${apiHost}/teamselect/`, fetchConfig);

			if (response.ok) {
				const active_team_id = await response.json();
				userdata.update((data) => ({ ...data, ...active_team_id }));
				goto('/game/join');
			} else {
				message = 'Oop! Something went wrong!'
			}
		}
	};
</script>

<svelte:head><title>TriviaMafia | Team Select</title></svelte:head>

<h1>Create a New Team</h1>
<button 
	class="button button-red"
	class:disabled={!hidecreateteam}
	on:click={() => hidecreateteam = !hidecreateteam}
>Create a New Team</button>

<form class:hidecreateteam>
	<h3>Enter Your Team Name</h3>
	<div class="input-element">
		<input type="text" placeholder="Team Name" />
	</div>
	<input class="button button-white" type="submit" name="" id="" value="Submit" />
</form>

<form on:submit|preventDefault={handleTeamSelectSubmit}>
	<h1 class="existing-team">Or Play with an Existing Team</h1>
	{#if message}<p class="error">{message}</p>{/if}
	<!-- TODO: on:focus, clear the message -->
	<label class="select-label" for="team-select">Choose A Team</label>
	<select class="select" id="team-select" name="team-select" bind:value={selected}>
		{#each $userteams as team (team.team_id)}
			<option value={team}>{team.team_name}</option>
		{/each}
	</select>
	<input class="button button-red" type="submit" value="Choose This Team" />
</form>

<button
	class="button button-black"
	class:disabled={!hideteampassword}
	on:click={() => hideteampassword = !hideteampassword}
>Enter Team Password</button>
<form class:hideteampassword>
	<div class="input-element">
		<input type="text" placeholder="Team Password" />
	</div>
	<input class="button button-white" type="submit" name="" id="" value="Submit" />
</form>

<style lang="scss">
	form {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
	}
	.input-element {
		width: 100%;
	}
	.existing-team {
		width: 110%;
		text-align: center;
		align-self: center;
	}
	h1, h3 {
		margin: .5em 0;
	}
	select {
		margin-bottom: 1em;
	}
	.select-label {
		margin-top: 1em;
	}
	.hidecreateteam {
		display: none;
	}
	.hideteampassword {
		display: none;
	}
</style>
