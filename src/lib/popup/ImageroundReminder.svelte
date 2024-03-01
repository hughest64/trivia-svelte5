<script lang="ts">
    import '$lib/styles/popup.scss';
    import { page } from '$app/stores';
    import CloseButton from './CloseButton.svelte';
    import { getStore, setEventCookie } from '$lib/utils';

    const popupData = getStore('popupData');
    const activeEventData = getStore('activeEventData');

    const setRoundAndResetPopup = () => {
        activeEventData.set({
            activeQuestionKey: '4.1',
            activeRoundNumber: 4,
            activeQuestionNumber: 1
        });
        setEventCookie($activeEventData, $page.params.joincode);

        resetPopup();
    };
    const resetPopup = () => {
        $popupData = { is_displayed: false, popup_type: '' };
    };
</script>

<div class="pop-timer" />
<div class="pop-content">
    <h3>Reminder!</h3>
    <h3>Don’t forget to finish your Image Round!</h3>
    <!-- <a href="/game/{$page.params.joincode}/" on:click={setRoundAndResetPopup}> Go to the Image Round </a> -->
</div>

<CloseButton on:click={resetPopup} />

<style lang="scss">
    .pop-content {
        padding-top: 0.75em;
        & * {
            padding: 0.25rem;
        }
    }
</style>
