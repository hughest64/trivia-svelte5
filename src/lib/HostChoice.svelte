<script lang="ts">
    import { userdata } from '../stores/user'
    import { goto } from '$app/navigation'

    // $: console.log('host choice', $userdata)
    export let hostchoice: string;

</script>

<div class="container">
    <h2>Would You Like to Host or Play?</h2>
    <button on:click={() => hostchoice="host"}>Host</button>
    <button on:click={() => hostchoice="play"}>Play</button>
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: .75em;
        max-width: 30rem;
        margin: 5rem auto 0;
    }
</style>