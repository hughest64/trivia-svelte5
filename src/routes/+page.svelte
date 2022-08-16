<script lang="ts">
    import { goto } from '$app/navigation';
    import HostChoice from '$lib/HostChoice.svelte';
    import TeamSelect from '$lib/TeamSelect.svelte';
    import { userdata } from '$stores/user';

    let hostchoice = 'choose'; // or 'play' or 'host'

    const handleChoiceClick = (event: MouseEvent) => {
        const target = <HTMLButtonElement>event.target;
        const id = target.id;
        if (id === 'host') {
            goto('/host/event-setup');
        }
        if (id === 'play') {
            hostchoice = 'play';
            goto('/');
        }
    };

    let historyIndex = 0;
    const handlepopstate = (event: PopStateEvent) => {
        const eventIndex = event.state['sveltekit:index'] || 0;

        // back
        if (historyIndex === 0 || eventIndex < historyIndex) {
            hostchoice = 'choose';

            // forward
        } else if (historyIndex !== 0 && eventIndex > historyIndex) {
            hostchoice = 'play';
        }
        historyIndex = eventIndex;
    };
</script>

<svelte:window on:popstate={handlepopstate} />

{#if ($userdata?.username && !$userdata?.is_staff) || hostchoice === 'play'}
    <TeamSelect />
{:else}
    <HostChoice on:click={handleChoiceClick} />
{/if}
