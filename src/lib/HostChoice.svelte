<script lang="ts">
    import { userdata } from '../stores/user'
    import { goto } from '$app/navigation'


</script>

<div class="container">
    <h2>Would You Like to Host or Play?</h2>
    <button id="host" on:click>Host</button>
    <button id="play" on:click>Play</button>
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