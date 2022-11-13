<script lang="ts">
    import '$lib/styles/popup.scss';
    import { page } from '$app/stores';
    import { fly } from 'svelte/transition';
    import { getStore, getCurrentFromKey } from '$lib/utils';
    import type { ActiveEventData, PopupData } from '$lib/types';

    const userData = $page.data.user_data;

    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: popupData = getStore<PopupData>('popupData');
    $: displayPopup = $popupData?.is_displayed;
    $: popupType = $popupData?.popup_type;
    $: count = $popupData.timer_value || 0;

    let interval: ReturnType<typeof setTimeout>;
    const countDown = async () => {
        if (count > 0) {
            count--;
            setTimeout(countDown, 1000);
        } else {
            clearTimeout(interval);
            if (userData?.auto_reveal_questions && !$page.url.pathname.startsWith('/host')) {
                const updatedData = getCurrentFromKey($popupData.data?.key);
                $activeEventData = {
                    activeQuestionKey: updatedData.question_key,
                    activeRoundNumber: updatedData.round_number,
                    activeQuestionNumber: updatedData.question_number
                };
                await fetch('/update', {
                    method: 'post',
                    body: JSON.stringify({ activeData: $activeEventData, joincode: $page.params.joincode })
                });
            }
            $popupData = { is_displayed: false, popup_type: '' };
        }
    };
    $: popupType === 'question_reveal' && setTimeout(countDown, 1000);
</script>

{#if displayPopup}
    <div class="pop" transition:fly={{ y: -200, duration: 800 }}>
        <div class="pop-timer">
            <!-- if there is a counter -->
            <h4>{count}</h4>
            <!-- <div> -->
            <!-- svg.pop-timer-svg > g.pop-timer-circle > circle.pop-timer-path-elapsed + path#pop-timer-path-remaining -->
            <!-- <span class="counter-value">5</span> -->
            <!-- </div> -->
        </div>
        <div class="pop-content">
            <!-- <h4>Title</h4> -->
            <!-- <h4>Message - Bold</h4> -->
            <p>The Next Question Will Be Revealed in {count} second{count > 1 ? 's' : ''}</p>
            <!-- button for cases that require use interaction -->
        </div>
        <button class="dismiss" on:click={() => (displayPopup = false)}>X</button>
    </div>
{/if}
