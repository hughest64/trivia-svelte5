<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from '$lib/utils';
    import type { ActiveEventData } from '$lib/types';

    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: activeQuestion = $page.data.questions?.find((q) => q.key === $activeEventData.activeQuestionKey);
    let hidden = true;
</script>

<!-- TODO: nice transition here when revealing the input component, it's also still styled poorly -->
<div id="notes-container" class="notes-container flex-column">
    <button class="button disabled" on:click={() => (hidden = !hidden)}>
        Notes for {activeQuestion?.key}
    </button>

    <form class:hidden on:submit|preventDefault>
        <div class="input-container">
            <input name="note" type="text" placeholder="Add a New Note" />
            <!-- <label for="note">Add a New Note</label> -->
        </div>
    </form>
</div>

<style lang="scss">
    .hidden {
        display: none;
    }
</style>
