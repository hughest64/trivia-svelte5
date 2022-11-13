<script lang="ts">
    import '$lib/styles/popup.scss';
    import { page } from '$app/stores';
    import { fly } from 'svelte/transition';
    import { getStore } from '$lib/utils';
    import type { PopupData } from '$lib/types';

    const userData = $page.data.user_data;

    $: popupData = getStore<PopupData>('popupData');
    $: displayPopup = $popupData?.is_displayed;
    $: popupType = $popupData?.popup_type;
    $: count = $popupData.timer_value || 0;

    // TODO:
    // - helper to create round and quesiton from key
    // - bring in active event data
    // - if !host route and auto_reveal === true
    // - set active data
    // - post to /update w/ active data
    let interval: ReturnType<typeof setTimeout>;
    const countDown = () => {
        if (count > 0) {
            count--;
            setTimeout(countDown, 1000);
        } else {
            clearTimeout(interval);
            console.log(
                `auto reveal? ${userData?.auto_reveal_questions},
                 if so, go to ${$popupData.data?.key} if ${$page.url.pathname} does not contain 'host'`
            );
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
