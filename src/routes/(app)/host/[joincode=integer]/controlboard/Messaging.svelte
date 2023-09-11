<script lang="ts">
    import { page } from '$app/stores';
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';

    const form = $page.form;

    const messages = getStore('chatMessages');
    $: console.log($messages);
</script>

<h1>Message Players</h1>

<div class="chat-form">
    <form action="" method="post" use:enhance>
        {#if form?.error}<p class="error">{form?.error}</p>{/if}
        <div class="input-container">
            <input type="text" name="chat_message" id="chat_message" required />
            <label for="chat_message">Send a Group Message</label>
        </div>
    </form>
</div>

<style lang="scss">
    .chat-form {
        form {
            width: var(--max-element-width);
        }
    }
</style>
