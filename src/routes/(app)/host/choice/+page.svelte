<script lang="ts">
    import { goto } from '$app/navigation';
    import { userdata } from '$stores/user';
    $: username = $userdata?.username || '';
</script>

<svelte:head><title>Trivia Mafia | Host Choice</title></svelte:head>

<h1>Greetings {username}</h1>
<h3>Do you want to:</h3>
<button class="button button-red" id="host" on:click={() => goto('/host/event-setup')}>Host A Game</button>
<button class="button button-black" id="play" on:click={() => goto('/team')}>Play Trivia</button>
<small>To view the recent changes in the application, click Here.</small>

<style>
    h1,
    h3 {
        margin: 0.75em 0;
    }
    small {
        padding: 0 0.5em;
        font-size: 12px;
    }
</style>