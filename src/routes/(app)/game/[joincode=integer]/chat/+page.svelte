<script lang="ts">
    import { getStore } from '$lib/utils';
    import type { ChatMessage } from '$lib/types';

    const user = getStore('userData');
    const chats = getStore('chatMessages');
    // TODO: temp for dev
    const member_chat: ChatMessage = {
        id: 75,
        username: 'Team Member',
        userid: 9999,
        chat_message: 'An example for a different user',
        team: 'todd rules',
        time: '4:00:00 PM'
    };
    $: chats.update((chats) => {
        const newchats = chats.filter((c) => c.id !== 75);
        newchats.splice(2, 0, member_chat);
        return newchats;
    });
</script>

<h1>Team Chat</h1>

<ul class="chat-container">
    {#each $chats as chat (chat.id)}
        <li class="chat-message {chat.userid === $user.id ? 'user-chat' : 'member-chat'}">
            <p>{chat.chat_message}</p>
            <small>{chat.username} {chat.time}</small>
        </li>
    {/each}
</ul>

<!-- TODO: form for chat submission -->

<style lang="scss">
    .chat-container {
        width: 60%;
        display: flex;
        flex-direction: column;
        row-gap: 1rem;
    }
    .chat-message {
        border: 2px solid var(--color-secondary);
        border-radius: 1.5rem;
        padding: 0.75rem;
        position: relative;

        p {
            margin: 0.25rem 0 0.25rem;
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
</style>
