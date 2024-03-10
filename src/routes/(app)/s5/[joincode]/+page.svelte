<script lang="ts">
    import { getContext } from 'svelte';
    import { enhance } from '$app/forms';
    import type { GameState } from './stores.svelte';

    const { current_event_data, locked_rounds, max_locked_round } = getContext<GameState>('gameState');
    $inspect(locked_rounds);
</script>

<main>
    <h1>Hello Svelte 5!</h1>
    <h4>The Current Question Key is: {current_event_data?.question_key}</h4>
    <h4>Locked Round(s):</h4>
    <p>{locked_rounds.join(', ')}</p>

    <form action="" method="post" use:enhance>
        <input type="hidden" name="round_to_lock" value={max_locked_round + 1} />
        <button class="button button-primary">Lock Round {max_locked_round + 1}</button>
    </form>
</main>
