<script lang="ts">
    import { page } from '$app/stores';
    import { createUserStore } from '$stores/user';
    import { createResponseStore } from '$stores/response';

    createResponseStore();

    $: $page.data?.user_data && createUserStore($page.data.user_data);
</script>

<slot />