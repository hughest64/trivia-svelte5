<script lang="ts">
    import { setContext } from 'svelte';
    import Socket from './Socket.svelte';
    import { GameState } from './stores.svelte';

    export let data: App.PageData;
    const { round_states, question_states, current_event_data } = data;
    setContext('gameState', new GameState(round_states || [], question_states, current_event_data));
</script>

<Socket>
    <slot />
</Socket>
