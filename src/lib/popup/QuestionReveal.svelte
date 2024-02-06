<script lang="ts">
    import '$lib/styles/popup.scss';
    import { fly } from 'svelte/transition';
    import CloseButton from './CloseButton.svelte';
    import { getStore } from '$lib/utils';
    const popupData = getStore('popupData');

    $: count = $popupData.timer_value || 0;

    const resetPopup = () => ($popupData = { is_displayed: false, popup_type: '' });

    let interval: ReturnType<typeof setTimeout>;
    const countDown = () => {
        if (count > 0) {
            count--;
            setTimeout(countDown, 1000);
        } else {
            clearTimeout(interval);
            // gotoQuestion();
            resetPopup();
        }
    };

    $: $popupData?.popup_type === 'question_reveal' && setTimeout(countDown, 1000);
</script>

<div class="pop-timer">
    {#key count}
        <h4 in:fly={{ y: -20 }}>{count}</h4>
    {/key}
</div>

<div class="pop-content">
    <p>
        The Next Question Will Be Revealed in
        {#key count}
            <span style="display: inline-block" in:fly={{ y: -20 }}>{count}</span>
        {/key} Second{count === 1 ? '' : 's'}
    </p>
</div>

<CloseButton on:click={() => (count = 0)} />
