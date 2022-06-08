<script>
    import { onMount } from 'svelte'
    import { goto } from '$app/navigation';
    import { userdata } from '../stores/user'

    onMount(async() => {
        !$userdata.is_staff && goto('/team-select')
    })
</script>

{#if $userdata.is_staff}
    <div class="container">
        <h2>Would You Like to Host or Play?</h2>
        <a href="/event-select">Host</a>
        <a href="/team-select">Play</a>
    </div>
{/if}

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