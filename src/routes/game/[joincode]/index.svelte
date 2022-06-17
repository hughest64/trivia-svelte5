<script lang="ts">
    // TODO: all of this should probably be in __layout
    import { page } from '$app/stores'
    import { eventData } from '../../../stores/event'

    const joincode = $page.params.joincode

</script>
<h1>Welcome to Game {joincode}</h1>

<div class="container">
    {#if $eventData}
        <pre>
            {JSON.stringify($eventData, null, 4)}
        </pre>
    {:else}
        <h3>No Data!</h3>
    {/if}
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