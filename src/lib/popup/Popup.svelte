<script lang="ts">
    import { fly } from 'svelte/transition';
    import QuestionReveal from './QuestionReveal.svelte';
    import ConfirmRoundUnlock from './ConfirmRoundUnlock.svelte';
    import { getStore } from '$lib/utils';
    import type { SvelteComponent } from 'svelte';
    import type { PopupData } from '$lib/types';

    $: popupData = getStore<PopupData>('popupData');

    type PopupMap = Record<string, typeof SvelteComponent>;
    const components: PopupMap = {
        'question_reveal': QuestionReveal,
        'round_unlock': ConfirmRoundUnlock
    };

</script>

<div class="pop" transition:fly={{ y: -200, duration: 800 }}>
        <!-- placed here as a template only, actual popup content should be rendered as a separate component from the popup map -->
        <!-- <div class="pop-timer">
            <h4>timer count</h4>
            <div>
                svg for timer path: svg.pop-timer-svg > g.pop-timer-circle > circle.pop-timer-path-elapsed + path#pop-timer-path-remaining
                <span class="counter-value">5</span>
            </div>
        </div> -->
        <!-- <div class="pop-content">
            <h4>Title</h4>
            <h4>Message - Bold</h4>
            <p>Message Text</p>
            button for cases that require use interaction
        </div> -->
    <svelte:component this={components[$popupData.popup_type]} />
</div>