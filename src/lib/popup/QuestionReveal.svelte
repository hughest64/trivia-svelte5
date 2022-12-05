<script lang="ts">
    import '$lib/styles/popup.scss';
    import { fly } from 'svelte/transition';
    import { page } from '$app/stores';
    import CloseButton from './CloseButton.svelte';
    import { getStore, getCurrentDataFromKey } from '$lib/utils';
    import type { ActiveEventData, PopupData } from '$lib/types';

    const userData = $page.data.user_data;

    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: popupData = getStore<PopupData>('popupData');
    $: count = $popupData.timer_value || 0;

    const resetPopup = () => ($popupData = { is_displayed: false, popup_type: '' });
    const gotoQuestion = async () => {
        if (userData?.auto_reveal_questions && !$page.url.pathname.startsWith('/host')) {
            const updatedData = getCurrentDataFromKey($popupData.data?.key);
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
    };

    let interval: ReturnType<typeof setTimeout>;
    const countDown = () => {
        if (count > 0) {
            count--;
            setTimeout(countDown, 1000);
        } else {
            clearTimeout(interval);
            gotoQuestion();
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
        {/key} second{count === 1 ? '' : 's'}
    </p>
</div>

<CloseButton on:click={() => (count = 0)} />
