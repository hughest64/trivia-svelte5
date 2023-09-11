<script lang="ts">
    import { afterUpdate } from 'svelte';
    import { page } from '$app/stores';
    import { browser } from '$app/environment';
    import { enhance } from '$app/forms';
    import { getStore } from '$lib/utils';

    $: form = $page.form;

    const user = getStore('userData');
    const chatMessages = getStore('chatMessages');

    const scrollToBottom = () => {
        if (!browser) return;
        window.scroll({ top: document.body.scrollHeight, behavior: 'smooth' });
    };
    afterUpdate(scrollToBottom);
</script>

<h1 class="page-header">Team Chat</h1>

<ul class="chat-container" id="chat-container">
    {#each $chatMessages as chat (chat.id)}
        <li class="chat-message {chat.userid === $user.id && !chat.is_host_message ? 'user-chat' : 'member-chat'}">
            {#each chat.chat_message.split('\n') as msg}
                <p>{msg}</p>
            {/each}
            <small>{chat.username} {chat.time}</small>
        </li>
    {/each}
</ul>

<div class="chat-form">
    <form action="" method="post" use:enhance>
        {#if form?.error}<p class="error">{form?.error}</p>{/if}
        <div class="input-container">
            <input type="text" name="chat_message" id="chat_message" required />
            <label for="chat_message">Chat with your Team</label>
        </div>
    </form>
</div>

<style lang="scss">
    .page-header {
        position: fixed;
        top: 0rem;
        margin: 0;
        padding: 1rem;
        width: 100%;
        text-align: center;
        background-color: var(--color-tertiary);
        z-index: 1;
    }
    .chat-container {
        position: relative;
        width: 60%;
        display: flex;
        margin: 0;
        padding: 5rem 1.5rem 0;
        margin-bottom: 8rem;
        flex-direction: column;
        row-gap: 1rem;
        overflow-x: auto;
    }
    .chat-message {
        border: 2px solid var(--color-secondary);
        border-radius: 1.5rem;
        padding: 0.75rem;
        position: relative;

        p {
            margin: 0.3rem 0;
        }

        small {
            margin-left: 0.25rem;
            font-size: 0.75rem;
        }
    }
    .user-chat {
        border-top-right-radius: 0;
        align-self: flex-end;
        background-color: var(--color-alt-white);
        ::after {
            content: '';
            background-color: var(--color-alt-white);
            position: absolute;
            left: auto;
            right: -13px;
            top: -2px;
            width: 1.5rem;
            height: 1.5rem;
            border-style: solid;
            border-width: 2px 2px 0 0;
            border-top-right-radius: 0;
            transform: skew(-45deg);
        }
    }
    .member-chat {
        border-top-left-radius: 0;
        align-self: flex-start;
        border-color: var(--color-teammate-chat);
        background-color: var(--color-alt-white);
        ::before {
            content: '';
            background-color: var(--color-alt-white);
            position: absolute;
            right: auto;
            left: -13px;
            top: -2px;
            width: 1.5rem;
            height: 1.5rem;
            border-style: solid;
            border-color: var(--color-teammate-chat);
            border-width: 2px 0 0 2px;
            border-top-right-radius: 0;
            transform: skew(45deg);
        }
    }
    .chat-form {
        position: fixed;
        bottom: var(--footer-height);
        width: calc(100% - 2rem);
        display: flex;
        justify-content: center;
        background-color: var(--color-tertiary);
        form {
            width: var(--max-element-width);
        }
    }

    @media (max-width: 1000px) {
        .chat-container {
            width: 100%;
        }
    }
</style>
