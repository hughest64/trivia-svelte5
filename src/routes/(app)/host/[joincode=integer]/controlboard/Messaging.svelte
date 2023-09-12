<script lang="ts">
    import { page } from '$app/stores';
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';

    const form = $page.form;

    const messages = getStore('chatMessages');
</script>

<form action="?/megaround_reminder" method="post" use:enhance>
    <button type="submit" class="button-tertiary button"> Send Megaround Warning </button>
</form>

<div class="chat-form">
    <form action="?/send_chat" method="post" use:enhance>
        {#if form?.error}<p class="error">{form?.error}</p>{/if}
        <div class="input-container">
            <input type="text" name="chat_message" id="chat_message" required />
            <label for="chat_message">Send a Group Message</label>
        </div>
    </form>
</div>

<ul>
    {#each $messages as msg (msg.id)}
        <li>{msg.chat_message}</li>
    {/each}
</ul>

<style lang="scss">
    .chat-form {
        form {
            width: var(--max-element-width);
        }
    }
    ul {
        list-style: inside;
    }
</style>
