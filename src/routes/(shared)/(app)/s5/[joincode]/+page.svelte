<script lang="ts">
    import { getContext } from 'svelte';
    import { enhance } from '$app/forms';
    import type { GameState } from '$lib/state/gameState.svelte';

    let gs = getContext<GameState>('gameState');
    $inspect(gs.locked_rounds);
</script>

<main>
    <h1>Hello Svelte 5!</h1>
    <h4>The Current Question Key is: {gs.current_event_data?.question_key}</h4>
    <h4>Locked Round(s):</h4>
    <p>{gs.locked_rounds.join(', ')}</p>

    <form action="" method="post" use:enhance>
        <input type="hidden" name="round_to_lock" value={gs.max_locked_round + 1} />
        <button class="button button-primary">Lock Round {gs.max_locked_round + 1}</button>
    </form>
</main>
