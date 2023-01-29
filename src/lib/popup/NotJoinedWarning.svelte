<script lang="ts">
    import '$lib/styles/popup.scss';
    import CloseButton from './CloseButton.svelte';
    import { getStore } from '$lib/utils';
    import type { PopupData } from '$lib/types';

    $: popupData = getStore<PopupData>('popupData');
    // TODO: this should be imported form a reusable place, or have a default on the Popup container
    const resetPopup = () => ($popupData = { is_displayed: false, popup_type: '' });
</script>

<div class="pop-timer" />
<div class="pop-content">
    <!-- TODO: better text here -->
    <h4>Not Joined to event</h4>
    <p>
        You are currently only viewing this event. Click the join button below to play or click the change team button
        to play with a different team
    </p>
    <div class="button-container">
        <!-- TODO: Post to the join action w/ the joincode, should this be a form? -->
        <button class="button button-red">Join Event</button>
        <!-- TODO: make this an ancor that goes to /team -->
        <button class="button button-red">Change Teams</button>
    </div>
</div>

<CloseButton on:click={resetPopup} />
