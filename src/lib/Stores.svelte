<script lang="ts">
    import { page } from '$app/stores';
    import { createUserStore } from '$stores/user';
    import { createResponseStore } from '$stores/response';

    createResponseStore();
    // TODO: hmmm, is this the right fallback? do we need one?
    createUserStore($page.data?.user_data || {});
</script>

<slot />