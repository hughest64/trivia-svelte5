<script lang="ts">
    import { fly } from 'svelte/transition';
    import QuestionReveal from './QuestionReveal.svelte';
    import ConfirmRoundUnlock from './ConfirmRoundUnlock.svelte';
    import { getStore } from '$lib/utils';
    import type { SvelteComponent } from 'svelte';

    const popupData = getStore('popupData');

    const components: Record<string, typeof SvelteComponent> = {
        question_reveal: QuestionReveal,
        round_unlock: ConfirmRoundUnlock
    };
</script>

{#if $popupData.is_displayed}
    <div class="pop" transition:fly={{ y: -200, duration: 800 }}>
        <svelte:component this={components[$popupData.popup_type]} />
    </div>
{/if}
