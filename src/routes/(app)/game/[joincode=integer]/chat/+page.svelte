<script lang="ts">
    import { getStore } from '$lib/utils';
    const chats = getStore('chatMessages');
    // $: console.log($chats);
</script>

<h1>Team Chat</h1>

<ul>
    {#each $chats as chat (chat.id)}
        <li>
            <div>
                <p>{chat.chat_message}</p>
                <small>{chat.username} {chat.time}</small>
            </div>
        </li>
    {/each}
</ul>

<!-- TODO: form for chat submission -->
