<script>
    import { onMount } from 'svelte'
    import { goto } from '$app/navigation';
    import { userdata } from '../../stores/user'
  
    // $: console.log('path', redirPath)
    $: console.log('ud', $userdata)

    // onMount(async() => {
    //     !$userdata.is_staff && goto('/game/team-select')
    // })
</script>

<!-- {#if $userdata.is_staff} -->
    <div class="container">
        <h2>Would You Like to Host or Play?</h2>
        <a href="/host/event-setup">Host</a>
        <a href="/game/team-select">Play</a>
    </div>
<!-- {/if} -->

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