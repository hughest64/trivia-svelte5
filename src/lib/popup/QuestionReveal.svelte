<script lang="ts">
    import '$lib/styles/popup.scss';
    import { page } from '$app/stores';
    import CloseButton from './CloseButton.svelte';
    import { getStore, getCurrentFromKey } from '$lib/utils';
    import type { ActiveEventData, PopupData } from '$lib/types';

    const userData = $page.data.user_data;

    $: activeEventData = getStore<ActiveEventData>('activeEventData');
    $: popupData = getStore<PopupData>('popupData');
    $: count = $popupData.timer_value || 0;

    const resetPopup = () => ($popupData = { is_displayed: false, popup_type: '' });
    const gotoQuestion = async () => {
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
    <h4>{count}</h4>
</div>

<div class="pop-content">
    <p>The Next Question Will Be Revealed in {count} second{count > 1 ? 's' : ''}</p>
</div>

<CloseButton on:click={() => (count = 0)} />
