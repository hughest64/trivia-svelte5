<script lang="ts">
    import { page } from '$app/stores';
    import { getStore } from './utils';
    import { deserialize } from '$app/forms';
    const userData = getStore('userData');

    $: autoRevealValue = !!$userData?.auto_reveal_questions;

    let formError = '';
    const handleAutoReveal = async (e: Event) => {
        formError = '';
        const target = e.target as HTMLFormElement;

        userData.update((data) => ({ ...data, auto_reveal_questions: !data.auto_reveal_questions }));

        const formData = new FormData();
        formData.set('auto_reveal', String(autoRevealValue));

        const response = await fetch(target.action, {
            method: 'post',
            body: formData
        });
        const result = deserialize(await response.text());
        if (result.type === 'failure') {
            formError = result.data?.error as string;
            userData.update((data) => ({ ...data, auto_reveal_questions: !data.auto_reveal_questions }));
        }
    };
</script>

<form action="/user/settings?/auto_reveal_update" method="post" on:submit|preventDefault={handleAutoReveal}>
    <label class="switch">
        <input type="checkbox" bind:checked={autoRevealValue} />
        <button class="slider round" />
    </label>
</form>

<style lang="scss">
    form {
        flex-direction: row;
        justify-content: flex-end;
    }
    .switch {
        position: relative;
        display: inline-block;
        width: 60px;
        height: 34px;
    }

    .switch input {
        opacity: 0;
        width: 0;
        height: 0;
    }

    .slider {
        position: absolute;
        cursor: pointer;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: var(--color-primary);
        -webkit-transition: 0.4s;
        transition: 0.4s;
    }

    .slider:before {
        position: absolute;
        content: '';
        height: 26px;
        width: 26px;
        left: 4px;
        bottom: 4px;
        background-color: white;
        -webkit-transition: 0.4s;
        transition: 0.4s;
    }

    input:checked + .slider {
        background-color: var(--color-current);
    }

    input:focus + .slider {
        box-shadow: 0 0 1px var(--color-current);
    }

    input:checked + .slider:before {
        -webkit-transform: translateX(26px);
        -ms-transform: translateX(26px);
        transform: translateX(26px);
    }

    .slider.round {
        border-radius: 34px;
    }

    .slider.round:before {
        border-radius: 50%;
    }
</style>
