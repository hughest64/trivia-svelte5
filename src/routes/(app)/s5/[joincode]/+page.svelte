<script lang="ts">
    import { getContext } from 'svelte';
    import type { GameState } from './stores.svelte';

    const { current_event_data, round_states, question_states } = getContext<GameState>('gameState');
    $inspect(round_states, question_states);
</script>

<main>
    <h1>Hello Svelte 5!</h1>
    <span>The Current Question Key is: {current_event_data?.question_key}</span>
</main>
