<script lang="ts">
    import '$lib/styles/popup.scss';
    import { fly } from 'svelte/transition';
    import { getStore } from '$lib/utils';
    import type { PopupData } from '$lib/types';

    $: popupData = getStore<PopupData>('popupData');
    $: displayPopup = $popupData?.is_displayed;
    $: popupType = $popupData?.popup_type;

    let interval: ReturnType<typeof setInterval>;
    let count = 5;
    const countDown = () => {
        console.log('countdown', count);
        // if (count > 0) {
        count--;
        // } 
    };
    
    $: popupType === 'question_reveal' && setInterval(countDown, 1000);
    $: if (count < 1) {
        console.log('clear me');
        clearInterval(interval);
    };
</script>

{#if displayPopup}
    <div class="pop" transition:fly={{ y: -2000, duration: 800 }}>
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
