<script lang="ts">
    import Socket from './Socket.svelte';

    export let data: App.PageData;
    const { round_states, question_states, current_event_data } = data;
    console.log(round_states);
</script>

<Socket>
    <slot />
</Socket>
