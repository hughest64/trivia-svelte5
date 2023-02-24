<script lang="ts">
    import { slide } from 'svelte/transition';
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import type { ActiveEventData } from '$lib/types';

    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: activeQuestion = $page.data.questions?.find((q) => q.key === $activeEventData.activeQuestionKey);
    let hidden = true;
</script>

<div id="notes-container" class="notes-container flex-column">
    <button class="button disabled" on:click={() => (hidden = !hidden)}>
        Notes for {activeQuestion?.key}
    </button>
    {#key hidden}
        <form transition:slide|local={{ duration: 200 }} class:hidden on:submit|preventDefault>
            <div id="note-container" class="input-container">
                <!-- TODO: note icon -->
                <input name="note" type="text" placeholder="Add a New Note" />
            </div>
        </form>
    {/key}
</div>

<style lang="scss">
    .hidden {
        display: none;
    }
</style>
